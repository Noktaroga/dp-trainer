"""
Paleta de colores moderna y profesional
"""

class ModernColors:
    """Colores base modernos"""
    
    # Tema Custom "Marino" (Reemplaza al Light original para aplicar cambios globales)
    # Inspirado en Visual Studio Dark / Navy theme con acentos pasteles
    LIGHT = {
        # Fondos (Marino Profundo)
        'bg_primary': '#0F172A',      # Slate 900 (Fondo Principal)
        'bg_secondary': '#0F172A',    # Fondo Ventana
        'bg_tertiary': '#1E293B',     # Slate 800 (Paneles laterales)
        
        # Superficies (Tarjetas)
        'surface': '#1E293B',         # Slate 800 (Tarjetas)
        'surface_elevated': '#334155', # Slate 700 (Hover)
        'surface_variant': '#334155',  # Compatibilidad
        
        # Primarios (Pastel Blue)
        'primary': '#60A5FA',         # Blue 400 (Cian/Azul Pastel)
        'primary_hover': '#93C5FD',   # Blue 300 (Más claro)
        'primary_light': '#172554',   # Blue 950 (Fondo de elementos seleccionados)
        
        # Secundarios (Pastel Purple)
        'secondary': '#A78BFA',       # Violet 400 (Lila Pastel)
        'secondary_hover': '#C4B5FD', 
        'secondary_light': '#4C1D95',
        
        # Estados (Pasteles sobre fondo oscuro)
        'success': '#34D399',         # Emerald 400 (Verde Pastel)
        'success_light': '#064E3B',   # Emerald 900 (Fondo Verde Oscuro)
        'warning': '#FBBF24',         # Amber 400 (Amarillo Pastel)
        'warning_light': '#451A03',   # Amber 900
        'error': '#F87171',           # Red 400 (Rojo Pastel)
        'error_light': '#7F1D1D',     # Red 900
        'info': '#38BDF8',            # Sky 400 (Celeste Pastel)
        'info_light': '#0C4A6E',      # Sky 900
        
        # Texto
        'text_primary': '#E2E8F0',    # Slate 200 (Blanco suave)
        'text_secondary': '#94A3B8',  # Slate 400 (Gris claro)
        'text_tertiary': '#64748B',   # Slate 500
        'text_inverse': '#0F172A',    # Texto oscuro para botones claros
        
        # Bordes
        'border': '#334155',          # Slate 700
        'border_hover': '#475569',    # Slate 600
        
        'accent_1': '#38BDF8',        # Cyan/Sky Blue
        'accent_2': '#818CF8',        # Indigo
        'accent_3': '#F472B6',        # Pink
        
        # Sombras
        'shadow_sm': 'rgba(0, 0, 0, 0.5)',
        'shadow_md': 'rgba(0, 0, 0, 0.7)',
        'shadow_lg': 'rgba(0, 0, 0, 0.9)',
    }
    
    # Referencia Dark (opcional)
    DARK = LIGHT.copy()


class Typography:
    """Tipografía moderna y legible"""
    
    # Familias de fuentes (Prioridad a Segoe UI / Inter)
    FONT_FAMILY_PRIMARY = '"Segoe UI", Inter, -apple-system, BlinkMacSystemFont, Roboto, sans-serif'
    FONT_FAMILY_MONO = 'Consolas, "JetBrains Mono", Monaco, monospace'
    
    # Tamaños
    SIZE_XS = 12
    SIZE_SM = 14
    SIZE_BASE = 16
    SIZE_LG = 18
    SIZE_XL = 20
    SIZE_2XL = 24
    SIZE_3XL = 30
    SIZE_4XL = 36
    SIZE_5XL = 48
    
    # Pesos
    WEIGHT_LIGHT = 300
    WEIGHT_NORMAL = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700
    
    # Alturas de línea
    LINE_HEIGHT_TIGHT = 1.25
    LINE_HEIGHT_NORMAL = 1.5
    LINE_HEIGHT_RELAXED = 1.75


class Spacing:
    """Sistema de espaciado consistente"""
    
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48
    XXXL = 64


class BorderRadius:
    """Radio de bordes redondeados"""
    
    SM = 6
    MD = 8
    LG = 12
    XL = 16
    FULL = 9999
