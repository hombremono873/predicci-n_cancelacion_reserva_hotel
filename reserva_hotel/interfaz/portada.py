"""Pantalla de inicio: descripción de la aplicación, sus funciones y los créditos del proyecto."""
import base64

import streamlit as st

from reserva_hotel.configuracion import CREDITOS, DESCRIPCION_APLICACION, FUNCIONES_APLICACION

# Íconos de línea fina en SVG (24 x 24), dibujados con el color de acento
ICONOS = {
    "hotel": (
        '<path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16"/><path d="M16 9h2a2 2 0 0 1 2 2v10"/>'
        '<path d="M2 21h20"/><path d="M8 7h4M8 11h4M8 15h4"/>'
    ),
    "reserva": (
        '<rect x="4" y="4" width="16" height="17" rx="2"/><path d="M8 2v4M16 2v4M4 10h16"/>'
        '<path d="M9 15l2 2 4-4"/>'
    ),
    "ajustes": (
        '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/>'
        '<circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>'
    ),
    "libro": (
        '<path d="M2 5h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 5h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/>'
    ),
    "graduacion": (
        '<path d="M22 9 12 4 2 9l10 5 10-5z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/>'
        '<path d="M22 9v6"/>'
    ),
}

ESTILOS = """
<style>
.portada { max-width: 960px; margin: 0 auto; text-align: center; font-family: inherit; }
.portada-encabezado { display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 8px; }
.portada-encabezado h1 { font-size: 2rem; font-weight: 600; margin: 0; color: #1f2328; }
.portada-descripcion { color: #57606a; font-size: 1.1rem; line-height: 1.6; margin: 16px auto 28px; max-width: 760px; }
.portada-funciones { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.portada-tarjeta { border: 1px solid #e3e6ea; border-radius: 12px; padding: 24px 20px; background: #ffffff; }
.portada-tarjeta h3 { font-size: 1.05rem; font-weight: 600; margin: 10px 0 6px; color: #1f2328; }
.portada-tarjeta p { color: #57606a; font-size: 0.95rem; line-height: 1.5; margin: 0; }
.portada-creditos { background: #f5f6f8; border-radius: 12px; padding: 28px 20px; margin-top: 28px; }
.portada-etiqueta { color: #2a78d6; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin: 10px 0 4px; }
.portada-universidad { font-size: 1.15rem; font-weight: 600; color: #1f2328; margin: 0; }
.portada-programa { color: #57606a; margin: 2px 0 0; }
.portada-nombres { font-size: 1.2rem; font-weight: 600; color: #1f2328; line-height: 1.6; margin: 0; }
.portada-detalle { color: #57606a; margin: 0; }
.portada-separador { width: 48px; border: 0; border-top: 1px solid #d0d7de; margin: 18px auto; }
</style>
"""


def dibujar_icono(nombre: str, tamano: int) -> str:
    """Devuelve un ícono de línea fina con el color de acento, como imagen SVG incrustada."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#2a78d6" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONOS[nombre]}</svg>'
    )
    # Streamlit no muestra el SVG escrito directamente en el HTML; como imagen sí lo muestra
    codificado = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{codificado}" width="{tamano}" height="{tamano}" alt="">'


def armar_tarjetas() -> str:
    """Arma una tarjeta por cada función de la aplicación."""
    tarjetas = ""
    for funcion in FUNCIONES_APLICACION:
        tarjetas = tarjetas + (
            '<div class="portada-tarjeta">'
            f'{dibujar_icono(funcion["icono"], 34)}'
            f'<h3>{funcion["titulo"]}</h3>'
            f'<p>{funcion["texto"]}</p>'
            "</div>"
        )
    return tarjetas


def armar_creditos() -> str:
    """Arma el bloque de créditos: universidad, programa, estudiantes, docente y fecha."""
    estudiantes = ""
    for estudiante in CREDITOS["estudiantes"]:
        estudiantes = estudiantes + f"{estudiante}<br>"
    return (
        '<div class="portada-creditos">'
        f'{dibujar_icono("graduacion", 34)}'
        f'<p class="portada-universidad">{CREDITOS["universidad"]}</p>'
        f'<p class="portada-programa">{CREDITOS["programa"]}</p>'
        '<hr class="portada-separador">'
        '<p class="portada-etiqueta">Estudiantes</p>'
        f'<p class="portada-nombres">{estudiantes}</p>'
        '<p class="portada-etiqueta">Docente</p>'
        f'<p class="portada-nombres">{CREDITOS["docente"]}</p>'
        '<hr class="portada-separador">'
        f'<p class="portada-detalle">{CREDITOS["fecha"]}</p>'
        "</div>"
    )


def entrar_a_la_aplicacion() -> None:
    """Marca la portada como vista para pasar a la aplicación."""
    st.session_state["portada_vista"] = True


def volver_a_la_portada() -> None:
    """Vuelve a mostrar la portada; al continuar, los campos empiezan otra vez con el ejemplo inicial."""
    del st.session_state["portada_vista"]


def mostrar_portada() -> None:
    """Muestra la pantalla de inicio con el botón para entrar a la aplicación."""
    st.html(
        ESTILOS
        + '<div class="portada">'
        + '<div class="portada-encabezado">'
        + dibujar_icono("hotel", 40)
        + "<h1>Riesgo de Cancelación de Reservas</h1>"
        + "</div>"
        + f'<p class="portada-descripcion">{DESCRIPCION_APLICACION}</p>'
        + f'<div class="portada-funciones">{armar_tarjetas()}</div>'
        + armar_creditos()
        + "</div>"
    )
    izquierda, centro, derecha = st.columns([1, 2, 1])
    with centro:
        st.button("Continuar", type="primary", width="stretch", on_click=entrar_a_la_aplicacion)
