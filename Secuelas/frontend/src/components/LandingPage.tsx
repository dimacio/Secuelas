import React, { useState, useEffect } from 'react';
import './LandingPage.css';

interface LandingPageProps {
  onStart: () => void;
}

const BOOT_LINES = [
  { text: "UEI SISTEMA v2.1.7 — INICIALIZANDO KERNEL...", delay: 0 },
  { text: "CARGANDO MÓDULOS DE CIFRADO AES-256...", delay: 420 },
  { text: "VERIFICANDO FIRMA DIGITAL DEL OPERADOR...", delay: 840 },
  { text: "CONECTANDO AL SERVIDOR CENTRAL [192.168.0.1]...", delay: 1260 },
  { text: "ESTABLECIENDO TÚNEL SEGURO... [OK]", delay: 1680 },
  { text: "COMPROBANDO NIVEL DE AUTORIZACIÓN...", delay: 2100 },
  { text: "ACCESO CONCEDIDO. BIENVENIDO, ANALISTA 734.", delay: 2600 },
];

const LandingPage: React.FC<LandingPageProps> = ({ onStart }) => {
  const [visibleLines, setVisibleLines] = useState<number>(-1);
  const [bootComplete, setBootComplete] = useState(false);
  const [contentVisible, setContentVisible] = useState(false);
  const [cursorVisible, setCursorVisible] = useState(true);

  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = [];

    BOOT_LINES.forEach((line, index) => {
      const t = setTimeout(() => {
        setVisibleLines(index);
      }, line.delay);
      timers.push(t);
    });

    const tDone = setTimeout(() => {
      setBootComplete(true);
      const tContent = setTimeout(() => {
        setContentVisible(true);
      }, 600);
      timers.push(tContent);
    }, 3400);
    timers.push(tDone);

    return () => timers.forEach(clearTimeout);
  }, []);

  useEffect(() => {
    if (bootComplete) return;
    const interval = setInterval(() => {
      setCursorVisible(v => !v);
    }, 530);
    return () => clearInterval(interval);
  }, [bootComplete]);

  return (
    <div className="landing-container">
      <div className="scanlines" />
      <div className="vignette" />

      {/* Boot sequence */}
      <div className={`boot-sequence ${bootComplete ? 'boot-done' : ''}`}>
        <div className="boot-header">
          ╔══════════════════════════════════════════════╗<br />
          ║   UNIDAD DE ESCRUTINIO INFORMATIVO — UEI     ║<br />
          ║   TERMINAL DE ACCESO CLASIFICADO v2.1.7      ║<br />
          ╚══════════════════════════════════════════════╝
        </div>
        <div className="boot-lines-container">
          {BOOT_LINES.map((line, i) => (
            <div
              key={i}
              className={`boot-line ${i <= visibleLines ? 'boot-line-visible' : 'boot-line-hidden'} ${i === BOOT_LINES.length - 1 && i === visibleLines ? 'boot-line-final' : ''}`}
            >
              <span className="boot-prefix">[{i < BOOT_LINES.length - 1 ? '  ' : 'OK'}]</span>
              {' '}{line.text}
            </div>
          ))}
          {!bootComplete && (
            <span className={`cursor-block ${cursorVisible ? 'cursor-on' : 'cursor-off'}`}>█</span>
          )}
        </div>
      </div>

      {/* Main landing content */}
      <div className={`landing-content ${contentVisible ? 'content-visible' : 'content-hidden'}`}>

        <div className="title-section">
          <div className="pre-title">◆ UNIDAD DE ESCRUTINIO INFORMATIVO ◆</div>

          <h1 className="main-title glitch" data-text="SECUELAS">SECUELAS</h1>

          <div className="post-title">
            TERMINAL DE ANALISTA — PROGRAMA DE ENTRENAMIENTO
          </div>
        </div>

        <div className="divider-line">
          {'─'.repeat(56)}
        </div>

        <div className="description-block">
          <p className="desc-line">En un estado donde cada byte es propiedad del régimen,</p>
          <p className="desc-line">usted es el <span className="highlight">Analista 734</span> — una pieza más del engranaje.</p>
          <p className="desc-line">Pero las consultas que ejecute revelarán más</p>
          <p className="desc-line">de lo que sus superiores quisieran.</p>
          <p className="desc-tagline">&gt; ¿Puede la verdad sobrevivir en un sistema que se alimenta de secretos? &lt;</p>
        </div>

        <div className="features-row">
          <div className="feature-item">
            <span className="feature-tag">[SQL]</span>
            <span className="feature-text">13 directivas de complejidad creciente</span>
          </div>
          <div className="feature-item">
            <span className="feature-tag">[NAR]</span>
            <span className="feature-text">Narrativa distópica cinematográfica</span>
          </div>
          <div className="feature-item">
            <span className="feature-tag">[MIS]</span>
            <span className="feature-text">Secretos que solo los datos revelan</span>
          </div>
        </div>

        <div className="cta-section">
          <button onClick={onStart} className="start-btn">
            <span className="btn-arrow">&gt;</span> INICIAR SIMULACIÓN <span className="btn-arrow">&lt;</span>
          </button>
          <p className="warning-text">
            ⚠ ADVERTENCIA: Todos los accesos son registrados y monitoreados por el Departamento de Control Interno.
          </p>
        </div>

        <div className="footer-classified">
          <span>PROTOCOLO SECUELAS</span>
          <span className="sep">|</span>
          <span>CLASIFICACIÓN: ULTRA-SECRETO</span>
          <span className="sep">|</span>
          <span>NIVEL DE AUTORIZACIÓN: 2</span>
        </div>

      </div>
    </div>
  );
};

export default LandingPage;
