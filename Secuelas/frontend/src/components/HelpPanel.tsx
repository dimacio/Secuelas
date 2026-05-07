import React, { useState } from 'react';
import './HelpPanel.css';

interface Example {
  description: string;
  code: string;
}

interface SubItem {
  label: string;
  description: string;
  examples: Example[];
}

interface Category {
  id: string;
  label: string;
  icon: string;
  items: SubItem[];
}

const MANUAL: Category[] = [
  {
    id: 'structure',
    label: 'Estructura de una consulta',
    icon: '①',
    items: [
      {
        label: 'Orden obligatorio de cláusulas',
        description: 'Las cláusulas SQL deben escribirse siempre en este orden. Invertirlas produce un error de sintaxis.',
        examples: [
          {
            description: 'Orden correcto completo',
            code:
`SELECT columnas
FROM tabla
WHERE condición
GROUP BY columna
HAVING condición_de_grupo
ORDER BY columna ASC/DESC
LIMIT n;`,
          },
          {
            description: 'Error típico — WHERE después de ORDER BY',
            code:
`-- ❌ INCORRECTO
SELECT * FROM empleados
ORDER BY nivel_acceso DESC
WHERE departamento = 'Análisis';

-- ✅ CORRECTO
SELECT * FROM empleados
WHERE departamento = 'Análisis'
ORDER BY nivel_acceso DESC;`,
          },
        ],
      },
      {
        label: 'Cláusulas opcionales',
        description: 'Solo SELECT y FROM son obligatorios. El resto se agrega según lo que necesites.',
        examples: [
          {
            description: 'Consulta mínima válida',
            code: 'SELECT * FROM empleados;',
          },
        ],
      },
    ],
  },
  {
    id: 'select',
    label: 'SELECT básico',
    icon: '▶',
    items: [
      {
        label: 'Seleccionar todas las columnas',
        description: 'Devuelve todas las columnas de una tabla.',
        examples: [{ description: 'Todos los empleados', code: 'SELECT *\nFROM empleados;' }],
      },
      {
        label: 'Seleccionar columnas específicas',
        description: 'Elige exactamente qué columnas mostrar.',
        examples: [{ description: 'Solo nombre y cargo', code: 'SELECT nombre, cargo\nFROM empleados;' }],
      },
      {
        label: 'Alias de columna (AS)',
        description: 'Renombra una columna en el resultado.',
        examples: [{ description: 'Calcular y nombrar', code: 'SELECT nombre,\n  precio * cantidad AS total\nFROM pedidos;' }],
      },
      {
        label: 'LIMIT — limitar filas',
        description: 'Restringe cuántas filas devuelve la consulta.',
        examples: [{ description: 'Solo los primeros 5', code: 'SELECT * FROM empleados\nLIMIT 5;' }],
      },
    ],
  },
  {
    id: 'where',
    label: 'Filtros (WHERE)',
    icon: '⧖',
    items: [
      {
        label: 'Igual / Distinto',
        description: '= compara valores exactos. != (o <>) excluye.',
        examples: [
          { description: 'Filtrar por departamento', code: "SELECT * FROM empleados\nWHERE departamento = 'Seguridad';" },
          { description: 'Excluir un valor', code: "SELECT * FROM empleados\nWHERE departamento != 'Consultoría';" },
        ],
      },
      {
        label: 'BETWEEN — rango numérico',
        description: 'Filtra valores entre dos límites (inclusivo).',
        examples: [{ description: 'Nivel de acceso 3 a 5', code: 'SELECT * FROM empleados\nWHERE nivel_acceso BETWEEN 3 AND 5;' }],
      },
      {
        label: 'LIKE — coincidencia de texto',
        description: '% reemplaza cualquier cantidad de caracteres. _ reemplaza uno solo.',
        examples: [
          { description: 'Titulo que contiene "Protocolo"', code: "SELECT * FROM documentos\nWHERE titulo LIKE '%Protocolo%';" },
          { description: 'Nombre que empieza con "A"', code: "SELECT * FROM empleados\nWHERE nombre LIKE 'A%';" },
        ],
      },
      {
        label: 'IN — lista de valores',
        description: 'Coincide si el valor está en una lista.',
        examples: [{ description: 'Varias estaciones', code: "SELECT * FROM registros_metro\nWHERE estacion IN ('Plaza Central', 'Ministerio');" }],
      },
      {
        label: 'IS NULL / IS NOT NULL',
        description: 'Detecta campos vacíos (NULL) o no vacíos.',
        examples: [
          { description: 'Sin fecha de salida', code: 'SELECT * FROM registros_metro\nWHERE timestamp_salida IS NULL;' },
          { description: 'Con tarjeta asignada', code: 'SELECT * FROM empleados\nWHERE tarjeta_metro IS NOT NULL;' },
        ],
      },
      {
        label: 'AND / OR / NOT',
        description: 'Combina condiciones. AND requiere ambas, OR requiere al menos una.',
        examples: [{ description: 'Dos condiciones', code: "SELECT * FROM empleados\nWHERE departamento = 'Análisis'\n  AND nivel_acceso >= 3;" }],
      },
    ],
  },
  {
    id: 'order',
    label: 'Ordenamiento',
    icon: '↕',
    items: [
      {
        label: 'ORDER BY — ordenar resultados',
        description: 'ASC = ascendente (A→Z, 1→9). DESC = descendente (Z→A, 9→1).',
        examples: [
          { description: 'Por nivel descendente', code: 'SELECT * FROM empleados\nORDER BY nivel_acceso DESC;' },
          { description: 'Múltiples criterios', code: 'SELECT * FROM empleados\nORDER BY departamento ASC, nombre ASC;' },
        ],
      },
    ],
  },
  {
    id: 'aggregate',
    label: 'Agregación (GROUP BY)',
    icon: '∑',
    items: [
      {
        label: 'COUNT — contar filas',
        description: 'COUNT(*) cuenta todas las filas. COUNT(col) ignora NULL.',
        examples: [{ description: 'Contar accesos', code: 'SELECT empleado_nombre,\n  COUNT(*) AS total_accesos\nFROM registros_acceso\nGROUP BY empleado_nombre;' }],
      },
      {
        label: 'SUM / AVG / MAX / MIN',
        description: 'Calcula suma, promedio, máximo o mínimo de una columna.',
        examples: [{ description: 'Gasto total por depto', code: 'SELECT departamento,\n  SUM(monto) AS gasto_total,\n  MAX(monto) AS mayor_gasto\nFROM transacciones\nGROUP BY departamento;' }],
      },
      {
        label: 'HAVING — filtrar grupos',
        description: 'Como WHERE pero aplicado después del GROUP BY.',
        examples: [{ description: 'Grupos con más de 3', code: 'SELECT empleado_nombre,\n  COUNT(*) AS total\nFROM registros_acceso\nGROUP BY empleado_nombre\nHAVING COUNT(*) > 3;' }],
      },
      {
        label: 'COUNT DISTINCT',
        description: 'Cuenta valores únicos, evita duplicados.',
        examples: [{ description: 'Documentos únicos', code: 'SELECT empleado_nombre,\n  COUNT(DISTINCT documento_id) AS docs_unicos\nFROM registros_acceso\nGROUP BY empleado_nombre;' }],
      },
    ],
  },
  {
    id: 'join',
    label: 'Combinar tablas (JOIN)',
    icon: '⟕',
    items: [
      {
        label: 'INNER JOIN (JOIN)',
        description: 'Devuelve solo filas que tienen coincidencia en ambas tablas.',
        examples: [{ description: 'Empleado con su depto', code: 'SELECT e.nombre, d.nombre AS departamento\nFROM empleados e\nJOIN departamentos d\n  ON e.departamento_id = d.id;' }],
      },
      {
        label: 'LEFT JOIN',
        description: 'Devuelve todas las filas de la izquierda aunque no tengan coincidencia. Las columnas sin par quedan NULL.',
        examples: [{ description: 'Documentos sin acceso', code: 'SELECT d.titulo, ra.id AS acceso_id\nFROM documentos d\nLEFT JOIN registros_acceso ra\n  ON d.id = ra.documento_id\nWHERE ra.id IS NULL;' }],
      },
      {
        label: 'JOIN con tres tablas',
        description: 'Encadena múltiples JOINs para cruzar varias fuentes.',
        examples: [{ description: 'Cadena de tres tablas', code: 'SELECT e.nombre, ra.documento_id, rm.estacion_entrada\nFROM empleados e\nJOIN registros_acceso ra ON e.id = ra.empleado_id\nJOIN registros_metro rm ON e.tarjeta_metro = rm.tarjeta_id;' }],
      },
    ],
  },
  {
    id: 'subquery',
    label: 'Subconsultas',
    icon: '⊂',
    items: [
      {
        label: 'Subconsulta en WHERE',
        description: 'Usa el resultado de una consulta interna como filtro.',
        examples: [
          { description: 'Registros no en lista', code: "SELECT * FROM registros_metro\nWHERE tarjeta_id NOT IN (\n  SELECT tarjeta_metro\n  FROM empleados\n  WHERE tarjeta_metro IS NOT NULL\n);" },
        ],
      },
    ],
  },
];

interface HelpPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const HelpPanel: React.FC<HelpPanelProps> = ({ isOpen, onClose }) => {
  const [openCategory, setOpenCategory] = useState<string | null>(null);
  const [openItem, setOpenItem] = useState<string | null>(null);

  const toggleCategory = (id: string) => {
    setOpenCategory(prev => (prev === id ? null : id));
    setOpenItem(null);
  };

  const toggleItem = (key: string) => {
    setOpenItem(prev => (prev === key ? null : key));
  };

  return (
    <>
      {/* Overlay */}
      {isOpen && <div className="help-overlay" onClick={onClose} />}

      {/* Panel */}
      <aside className={`help-panel ${isOpen ? 'help-panel--open' : ''}`}>
        <div className="help-panel__header">
          <span className="help-panel__title">&#9632; MANUAL DEL AGENTE</span>
          <button className="help-panel__close" onClick={onClose} title="Cerrar">✕</button>
        </div>
        <p className="help-panel__subtitle">
          Referencia de sintaxis SQL — Uso interno UEI
        </p>

        <nav className="help-panel__nav">
          {MANUAL.map(cat => (
            <div key={cat.id} className="help-cat">
              <button
                className={`help-cat__btn ${openCategory === cat.id ? 'help-cat__btn--open' : ''}`}
                onClick={() => toggleCategory(cat.id)}
              >
                <span className="help-cat__icon">{cat.icon}</span>
                <span>{cat.label}</span>
                <span className="help-cat__arrow">{openCategory === cat.id ? '▲' : '▼'}</span>
              </button>

              {openCategory === cat.id && (
                <div className="help-cat__items">
                  {cat.items.map((item, idx) => {
                    const key = `${cat.id}-${idx}`;
                    return (
                      <div key={key} className="help-item">
                        <button
                          className={`help-item__btn ${openItem === key ? 'help-item__btn--open' : ''}`}
                          onClick={() => toggleItem(key)}
                        >
                          <span className="help-item__arrow">{openItem === key ? '▼' : '▶'}</span>
                          {item.label}
                        </button>

                        {openItem === key && (
                          <div className="help-item__content">
                            <p className="help-item__desc">{item.description}</p>
                            {item.examples.map((ex, ei) => (
                              <div key={ei} className="help-example">
                                <p className="help-example__label">{'// '}{ex.description}</p>
                                <pre className="help-example__code">{ex.code}</pre>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          ))}
        </nav>

        <div className="help-panel__footer">
          <span>CLASIFICACIÓN: USO INTERNO — UEI</span>
        </div>
      </aside>
    </>
  );
};

export default HelpPanel;
