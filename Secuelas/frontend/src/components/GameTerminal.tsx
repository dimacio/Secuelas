import React, { useState, useEffect, useCallback } from 'react';
import api from '../services/api'; // Axios instance for API calls
import './GameTerminal.css';

// TypeScript Interfaces for our data
interface Mission {
    id: number;
    title: string;
    coordinator_message_subject: string;
    coordinator_message_body: string;
}

interface GameState {
    mission: Mission | null;
    results: any[] | null;
    columns: string[] | null;
    error: string | null;
    last_query: string;
    archived_findings: string[];
    is_final_mission: boolean;
    mission_completed_show_results: boolean;
    flash_messages: [string, string][];
}

const GameTerminal: React.FC = () => {
    const [gameState, setGameState] = useState<GameState | null>(null);
    const [sqlQuery, setSqlQuery] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    const fetchGameState = useCallback(async () => {
        try {
            const response = await api.get<GameState>('/game_state');
            setGameState(response.data);
            setSqlQuery(response.data.last_query || '');
        } catch (error) {
            console.error("Error fetching game state:", error);
            // Handle critical error, maybe show a specific error message
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchGameState();
    }, [fetchGameState]);

    const handleSubmitQuery = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await api.post<GameState>('/submit_query', { sql_query: sqlQuery });
            setGameState(response.data);
        } catch (error) {
            console.error("Error submitting query:", error);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleNextMission = async () => {
        setIsLoading(true);
        try {
            const response = await api.post<GameState>('/next_mission');
            setGameState(response.data);
            setSqlQuery(''); // Clear textarea for next mission
        } catch (error) {
            console.error("Error proceeding to next mission:", error);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleReset = async () => {
        setIsLoading(true);
        if (window.confirm("¿Está seguro de que desea reiniciar todo el progreso?")) {
            try {
                const response = await api.post<GameState>('/reset_progress');
                setGameState(response.data);
                setSqlQuery('');
            } catch (error) {
                console.error("Error resetting progress:", error);
            }
        }
        setIsLoading(false);
    };

    if (isLoading && !gameState) {
        return <div className="terminal-container">Cargando Sistema...</div>;
    }
    
    if (!gameState || !gameState.mission) {
        return <div className="terminal-container">Error crítico del sistema. No se pudo cargar la misión.</div>;
    }

    const { 
        mission, results, columns, error, archived_findings, 
        is_final_mission, mission_completed_show_results, flash_messages 
    } = gameState;

    return (
        <div className="terminal-container">
            <header className="mb-6">
                <h1 className="text-3xl text-center border-b-2 border-[#00FF41] pb-2">TERMINAL DE ANALISTA - UNIDAD DE ESCRUTINIO INFORMATIVO</h1>
                {/* Header logic based on mission state */}
            </header>

            {flash_messages && flash_messages.map(([category, message], index) => (
                <div key={index} className={`flash-message flash-${category}`}>{message}</div>
            ))}
            
            <section id="mission-briefing" className="message-box">
                <h2 className="text-xl font-bold mb-2">
                    {mission_completed_show_results ? `[DIRECTIVA COMPLETADA: ${mission.title}]` : `[DIRECTIVA ACTUAL: ${mission.title}]`}
                </h2>
                <p className="text-sm mb-1"><strong>ASUNTO:</strong> {mission.coordinator_message_subject}</p>
                <hr className="border-[#00B32C] my-2" />
                <div className="whitespace-pre-wrap">{mission.coordinator_message_body}</div>
            </section>

            {mission_completed_show_results ? (
                 <section id="completed-mission-info" className="mt-4">
                     {/* Display query and results */}
                     <button onClick={handleNextMission} className="btn btn-next">CONTINUAR A LA SIGUIENTE DIRECTIVA</button>
                 </section>
            ) : (
                 <section id="sql-console">
                    <h3 className="text-lg mb-2">ENTRADA DE CONSULTA SQL:</h3>
                    <form onSubmit={handleSubmitQuery}>
                        <textarea 
                            value={sqlQuery}
                            onChange={(e) => setSqlQuery(e.target.value)}
                            className="console-input" 
                            rows={8} 
                            placeholder="Escriba su consulta SQL aquí..."
                            disabled={isLoading}
                        />
                        <button type="submit" className="btn" disabled={isLoading}>
                            {isLoading ? 'PROCESANDO...' : 'EJECUTAR CONSULTA'}
                        </button>
                    </form>
                </section>
            )}

            {error && !mission_completed_show_results && (
                 <section id="error-output" className="mt-4 p-3 bg-red-900 border border-red-500">
                    <h3 className="text-lg text-red-300">ERROR DE SISTEMA / CONSULTA:</h3>
                    <p className="text-red-200 whitespace-pre-wrap">{error}</p>
                </section>
            )}
            
            {results && columns && !error && !mission_completed_show_results && (
                <section id="query-results" className="mt-4">
                    <h3 className="text-lg mb-2">RESULTADOS DE LA CONSULTA:</h3>
                    <div className="overflow-x-auto">
                        <table className="results-table">
                            <thead>
                                <tr>{columns.map(col => <th key={col}>{col}</th>)}</tr>
                            </thead>
                            <tbody>
                                {results.map((row, rowIndex) => (
                                    <tr key={rowIndex}>
                                        {columns.map(col => <td key={`${rowIndex}-${col}`}>{row[col]}</td>)}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>
            )}

            {archived_findings && archived_findings.length > 0 && (
                 <section className="archived-findings">
                    <h3>HALLAZGOS ARCHIVADOS:</h3>
                    <ul>
                        {archived_findings.map((finding, index) => <li key={index}>{finding}</li>)}
                    </ul>
                </section>
            )}
            
            <footer className="mt-8 pt-4 border-t-2 border-[#00FF41] text-center">
                <button onClick={handleReset} className="btn bg-yellow-700 border-yellow-500 text-yellow-200 hover:bg-yellow-600">REINICIAR SIMULACIÓN</button>
                <p className="text-xs mt-3">Departamento de Control Interno - Todos los accesos son monitoreados.</p>
            </footer>
        </div>
    );
};

export default GameTerminal;

