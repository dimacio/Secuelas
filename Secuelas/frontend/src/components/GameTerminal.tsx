import React, { useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import HelpPanel from './HelpPanel';
import './GameTerminal.css';

interface Mission {
    id: number;
    title: string;
    coordinator_message_subject: string;
    coordinator_message_body: string;
}

interface GameState {
    mission: Mission | null;
    results: Record<string, unknown>[] | null;
    columns: string[] | null;
    error: string | null;
    last_query: string;
    archived_findings: string[];
    is_final_mission: boolean;
    mission_completed_show_results: boolean;
    flash_messages: [string, string][];
}

interface HintState {
    text: string | null;
    level: number;
    hasMore: boolean;
    exhausted: boolean;
}

function describeError(err: unknown): string {
    if (err && typeof err === 'object') {
        const e = err as Record<string, unknown>;
        if (e.response) {
            const res = e.response as Record<string, unknown>;
            const data = res.data as Record<string, unknown> | undefined;
            if (data?.error) return `Error del servidor (${res.status}): ${data.error}`;
            return `Error del servidor: HTTP ${res.status}`;
        }
        if (e.request) return 'Sin respuesta del servidor. Verifique que el backend esté corriendo en http://localhost:5001';
        if (e.message) return `Error de red: ${e.message}`;
    }
    return 'Error desconocido.';
}

const GameTerminal: React.FC = () => {
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [sqlQuery, setSqlQuery] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [loadError, setLoadError] = useState<string | null>(null);
    const [hint, setHint] = useState<HintState>({ text: null, level: 0, hasMore: true, exhausted: false });
    const [hintLoading, setHintLoading] = useState(false);
    const [helpOpen, setHelpOpen] = useState(false);

    const fetchGameState = useCallback(async () => {
        setIsLoading(true);
        setLoadError(null);
        try {
            const response = await api.get<GameState>('/game_state');
            setGameState(response.data);
            setSqlQuery(response.data.last_query || '');
        } catch (err) {
            console.error('Error fetching game state:', err);
            setLoadError(describeError(err));
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => { fetchGameState(); }, [fetchGameState]);

    // Reset hint state when mission changes
    const prevMissionId = React.useRef<number | null>(null);
    useEffect(() => {
        if (gameState?.mission && gameState.mission.id !== prevMissionId.current) {
            prevMissionId.current = gameState.mission.id;
            setHint({ text: null, level: 0, hasMore: true, exhausted: false });
        }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [gameState?.mission?.id]);

    const handleSubmitQuery = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await api.post<GameState>('/submit_query', { sql_query: sqlQuery });
            setGameState(response.data);
        } catch (err) {
            console.error('Error submitting query:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleNextMission = async () => {
        setIsLoading(true);
        setHint({ text: null, level: 0, hasMore: true, exhausted: false });
        try {
            const response = await api.post<GameState>('/next_mission');
            setGameState(response.data);
            setSqlQuery('');
        } catch (err) {
            console.error('Error next mission:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = async () => {
        if (!window.confirm('¿Está seguro de que desea reiniciar todo el progreso?')) return;
        setIsLoading(true);
        setHint({ text: null, level: 0, hasMore: true, exhausted: false });
        try {
            const response = await api.post<GameState>('/reset_progress');
            setGameState(response.data);
            setSqlQuery('');
        } catch (err) {
            console.error('Error resetting:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleRequestHint = async () => {
        if (hintLoading) return;
        setHintLoading(true);
        try {
            const res = await api.post<{ hint: string; level: number; has_more: boolean; exhausted?: boolean }>('/get_hint');
            const d = res.data;
            setHint({
                text: d.hint,
                level: d.level,
                hasMore: d.has_more ?? false,
                exhausted: d.exhausted ?? false,
            });
        } catch (err) {
            console.error('Error getting hint:', err);
        } finally {
            setHintLoading(false);
        }
    };

    // ── Loading / error ─────────────────────────────────────────────────────

    if (isLoading && !gameState) {
        return (
            <div className="terminal-container" style={{ textAlign: 'center', paddingTop: '4rem' }}>
                <p style={{ color: '#00FF41', fontSize: '1.2rem' }}>Iniciando sistema...</p>
            </div>
        );
    }

    if (loadError) {
        return (
            <div className="terminal-container" style={{ paddingTop: '4rem' }}>
                <h2 style={{ color: '#FF4444', marginBottom: '1rem' }}>⚠ ERROR CRÍTICO DEL SISTEMA</h2>
                <p style={{ color: '#FF8888', marginBottom: '1.5rem', fontFamily: 'monospace' }}>{loadError}</p>
                <p style={{ color: '#888', marginBottom: '1rem', fontSize: '0.85rem' }}>
                    Asegúrese de que Docker está corriendo y luego:
                </p>
                <pre style={{ color: '#00FF41', background: '#111', padding: '0.75rem', borderRadius: '4px', marginBottom: '1.5rem', fontSize: '0.85rem' }}>
                    docker-compose up --build
                </pre>
                <button className="btn" onClick={fetchGameState}>Reintentar conexión</button>
            </div>
        );
    }

    if (!gameState || !gameState.mission) {
        return (
            <div className="terminal-container" style={{ paddingTop: '4rem' }}>
                <h2 style={{ color: '#FF4444', marginBottom: '1rem' }}>⚠ MISIÓN NO DISPONIBLE</h2>
                <p style={{ color: '#888' }}>El servidor respondió pero no hay misiones cargadas.</p>
                <br />
                <button className="btn" onClick={fetchGameState}>Reintentar</button>
            </div>
        );
    }

    const {
        mission, results, columns, error, archived_findings,
        is_final_mission, mission_completed_show_results, flash_messages,
    } = gameState;

    // ── Final mission ───────────────────────────────────────────────────────

    if (is_final_mission) {
        return (
            <div className="terminal-container" style={{ textAlign: 'center', paddingTop: '4rem' }}>
                <h1 style={{ color: '#00FF41', fontSize: '2rem', marginBottom: '2rem' }}>✓ EVALUACIÓN CONCLUIDA</h1>
                <div className="message-box">
                    <p><strong>{mission.coordinator_message_subject}</strong></p>
                    <hr style={{ borderColor: '#00B32C', margin: '1rem 0' }} />
                    <p className="whitespace-pre-wrap">{mission.coordinator_message_body}</p>
                </div>
                <br />
                <button onClick={handleReset} className="btn">REINICIAR SIMULACIÓN</button>
            </div>
        );
    }

    // ── Main UI ─────────────────────────────────────────────────────────────

    return (
        <>
            <div className="terminal-container">
                <header className="mb-6">
                    <h1 className="text-3xl text-center border-b-2 border-[#00FF41] pb-2">
                        TERMINAL DE ANALISTA — UNIDAD DE ESCRUTINIO INFORMATIVO
                    </h1>
                </header>

                {/* Flash messages */}
                {flash_messages?.map(([category, message], i) => (
                    <div key={i} className={`flash-message flash-${category}`}>{message}</div>
                ))}

                {/* Mission briefing */}
                <section id="mission-briefing" className="message-box">
                    <h2 className="text-xl font-bold mb-2">
                        {mission_completed_show_results
                            ? `[DIRECTIVA COMPLETADA: ${mission.title}]`
                            : `[DIRECTIVA ACTUAL: ${mission.title}]`}
                    </h2>
                    <p className="text-sm mb-1">
                        <strong>ASUNTO:</strong> {mission.coordinator_message_subject}
                    </p>
                    <hr className="border-[#00B32C] my-2" />
                    <div className="whitespace-pre-wrap">{mission.coordinator_message_body}</div>
                </section>

                {/* Completed: show results + next button */}
                {mission_completed_show_results ? (
                    <section id="completed-mission-info" className="mt-4">
                        {results && columns && (
                            <div className="overflow-x-auto mb-4">
                                <h3 className="text-lg mb-2">RESULTADOS DE TU CONSULTA:</h3>
                                <table className="results-table">
                                    <thead>
                                        <tr>{columns.map(col => <th key={col}>{col}</th>)}</tr>
                                    </thead>
                                    <tbody>
                                        {results.map((row, ri) => (
                                            <tr key={ri}>
                                                {columns.map(col => (
                                                    <td key={`${ri}-${col}`}>{String(row[col] ?? '')}</td>
                                                ))}
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                        <button onClick={handleNextMission} className="btn btn-next" disabled={isLoading}>
                            {isLoading ? 'PROCESANDO...' : 'CONTINUAR A LA SIGUIENTE DIRECTIVA →'}
                        </button>
                    </section>
                ) : (
                    /* Active mission: SQL input */
                    <section id="sql-console" className="mt-4">
                        <h3 className="text-lg mb-2">ENTRADA DE CONSULTA SQL:</h3>
                        <form onSubmit={handleSubmitQuery}>
                            <textarea
                                value={sqlQuery}
                                onChange={e => setSqlQuery(e.target.value)}
                                className="console-input"
                                rows={8}
                                placeholder="Escriba su consulta SQL aquí..."
                                disabled={isLoading}
                            />
                            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', alignItems: 'center', marginTop: '8px' }}>
                                <button type="submit" className="btn" disabled={isLoading || !sqlQuery.trim()}>
                                    {isLoading ? 'PROCESANDO...' : 'EJECUTAR CONSULTA'}
                                </button>

                                {/* Hint button */}
                                {!hint.exhausted && (
                                    <button
                                        type="button"
                                        className="hint-btn"
                                        onClick={handleRequestHint}
                                        disabled={hintLoading}
                                        title={hint.level === 0 ? 'Solicitar primera pista' : 'Solicitar pista más específica'}
                                    >
                                        {hintLoading
                                            ? '...'
                                            : hint.level === 0
                                                ? '? SOLICITAR PISTA'
                                                : hint.hasMore
                                                    ? '?? PISTA MÁS ESPECÍFICA'
                                                    : '? SOLICITAR PISTA'}
                                    </button>
                                )}
                            </div>
                        </form>

                        {/* Hint display */}
                        {hint.text && (
                            <div className={`hint-box ${hint.exhausted ? 'hint-box--exhausted' : ''}`}>
                                <p className="hint-box__label">
                                    {hint.level === 1 ? '▸ PISTA NIVEL 1' : '▸▸ PISTA NIVEL 2'}{hint.exhausted ? ' (máximo alcanzado)' : ''}
                                </p>
                                <p className="hint-box__text">{hint.text}</p>
                            </div>
                        )}
                    </section>
                )}

                {/* SQL error */}
                {error && !mission_completed_show_results && (
                    <section className="mt-4 p-3" style={{ background: '#2d0000', border: '1px solid #FF4444' }}>
                        <h3 className="text-lg" style={{ color: '#FF8888' }}>ERROR DE CONSULTA:</h3>
                        <p className="whitespace-pre-wrap" style={{ color: '#FFAAAA', fontFamily: 'monospace' }}>{error}</p>
                    </section>
                )}

                {/* Query results */}
                {results && columns && !error && !mission_completed_show_results && (
                    <section id="query-results" className="mt-4">
                        <h3 className="text-lg mb-2">RESULTADOS ({results.length} filas):</h3>
                        <div className="overflow-x-auto">
                            <table className="results-table">
                                <thead>
                                    <tr>{columns.map(col => <th key={col}>{col}</th>)}</tr>
                                </thead>
                                <tbody>
                                    {results.map((row, ri) => (
                                        <tr key={ri}>
                                            {columns.map(col => (
                                                <td key={`${ri}-${col}`}>{String(row[col] ?? '')}</td>
                                            ))}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </section>
                )}

                {/* Archived findings */}
                {archived_findings && archived_findings.length > 0 && (
                    <section className="archived-findings mt-4">
                        <h3>HALLAZGOS ARCHIVADOS:</h3>
                        <ul>{archived_findings.map((f, i) => <li key={i}>{f}</li>)}</ul>
                    </section>
                )}

                <footer className="mt-8 pt-4 border-t-2 border-[#00FF41] text-center">
                    <button
                        onClick={handleReset}
                        className="btn"
                        style={{ background: '#3d2d00', border: '1px solid #FFB800', color: '#FFD580' }}
                        disabled={isLoading}
                    >
                        REINICIAR SIMULACIÓN
                    </button>
                    <p className="text-xs mt-3">Departamento de Control Interno — Todos los accesos son monitoreados.</p>
                </footer>
            </div>

            {/* Floating help button */}
            <button className="help-trigger" onClick={() => setHelpOpen(true)} title="Abrir Manual del Agente">
                <span className="help-trigger__icon">&#9632;</span>
                MANUAL DEL AGENTE
            </button>

            {/* Help panel */}
            <HelpPanel isOpen={helpOpen} onClose={() => setHelpOpen(false)} />
        </>
    );
};

export default GameTerminal;
