"""
Syntax Highlighter para SQL en tiempo real
Proporciona resaltado de sintaxis para comandos SQL en el Matrix Trainer
"""

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


class SQLSyntaxHighlighter(QSyntaxHighlighter):
    """Resaltador de sintaxis SQL en tiempo real"""
    
    def __init__(self, parent=None, theme='matrix'):
        super().__init__(parent)
        self.theme = theme
        self.highlighting_rules = []
        
        # Definir colores por tema
        self.themes = {
            'matrix': {
                'keyword': '#00FF00',
                'function': '#00DD00',
                'string': '#FFFF00',
                'number': '#00FFFF',
                'comment': '#006600',
                'operator': '#00FF88',
                'identifier': '#00DD00'
            },
            'cyberpunk': {
                'keyword': '#FF00FF',
                'function': '#00FFFF',
                'string': '#FFFF00',
                'number': '#FF6600',
                'comment': '#888888',
                'operator': '#FF0088',
                'identifier': '#00FFFF'
            },
            'classic': {
                'keyword': '#0000FF',
                'function': '#FF00FF',
                'string': '#A31515',
                'number': '#098658',
                'comment': '#008000',
                'operator': '#000000',
                'identifier': '#001080'
            }
        }
        
        self._setup_rules()
    
    def _setup_rules(self):
        """Configura las reglas de resaltado de sintaxis"""
        colors = self.themes.get(self.theme, self.themes['matrix'])
        
        # Palabras clave SQL
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(colors['keyword']))
        keyword_format.setFontWeight(QFont.Bold)
        
        keywords = [
            '\\bSELECT\\b', '\\bFROM\\b', '\\bWHERE\\b', '\\bINSERT\\b', '\\bINTO\\b',
            '\\bVALUES\\b', '\\bUPDATE\\b', '\\bDELETE\\b', '\\bCREATE\\b', '\\bTABLE\\b',
            '\\bALTER\\b', '\\bDROP\\b', '\\bINDEX\\b', '\\bVIEW\\b', '\\bJOIN\\b',
            '\\bINNER\\b', '\\bLEFT\\b', '\\bRIGHT\\b', '\\bOUTER\\b', '\\bON\\b',
            '\\bAND\\b', '\\bOR\\b', '\\bNOT\\b', '\\bNULL\\b', '\\bIS\\b',
            '\\bLIKE\\b', '\\bIN\\b', '\\bBETWEEN\\b', '\\bEXISTS\\b', '\\bCASE\\b',
            '\\bWHEN\\b', '\\bTHEN\\b', '\\bELSE\\b', '\\bEND\\b', '\\bGROUP\\b',
            '\\bBY\\b', '\\bHAVING\\b', '\\bORDER\\b', '\\bASC\\b', '\\bDESC\\b',
            '\\bLIMIT\\b', '\\bOFFSET\\b', '\\bUNION\\b', '\\bALL\\b', '\\bDISTINCT\\b',
            '\\bAS\\b', '\\bWITH\\b', '\\bRECURSIVE\\b', '\\bCTE\\b',
            '\\bPRIMARY\\b', '\\bKEY\\b', '\\bFOREIGN\\b', '\\bREFERENCES\\b',
            '\\bCONSTRAINT\\b', '\\bUNIQUE\\b', '\\bCHECK\\b', '\\bDEFAULT\\b',
            '\\bBIGINT\\b', '\\bINT\\b', '\\bINTEGER\\b', '\\bSMALLINT\\b', '\\bTINYINT\\b',
            '\\bVARCHAR\\b', '\\bCHAR\\b', '\\bTEXT\\b', '\\bNVARCHAR\\b', '\\bNCHAR\\b',
            '\\bDECIMAL\\b', '\\bNUMERIC\\b', '\\bFLOAT\\b', '\\bREAL\\b', '\\bDOUBLE\\b',
            '\\bDATE\\b', '\\bTIME\\b', '\\bDATETIME\\b', '\\bDATETIME2\\b', '\\bTIMESTAMP\\b',
            '\\bBOOLEAN\\b', '\\bBIT\\b', '\\bBLOB\\b', '\\bCLOB\\b'
        ]
        
        for keyword in keywords:
            pattern = QRegExp(keyword, Qt.CaseInsensitive)
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Funciones SQL
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(colors['function']))
        function_format.setFontWeight(QFont.Bold)
        
        functions = [
            '\\bCOUNT\\b', '\\bSUM\\b', '\\bAVG\\b', '\\bMIN\\b', '\\bMAX\\b',
            '\\bUPPER\\b', '\\bLOWER\\b', '\\bLEN\\b', '\\bLENGTH\\b', '\\bTRIM\\b',
            '\\bSUBSTRING\\b', '\\bREPLACE\\b', '\\bCONCAT\\b', '\\bCOALESCE\\b',
            '\\bCAST\\b', '\\bCONVERT\\b', '\\bGETDATE\\b', '\\bDATEDIFF\\b',
            '\\bDATEADD\\b', '\\bYEAR\\b', '\\bMONTH\\b', '\\bDAY\\b',
            '\\bROW_NUMBER\\b', '\\bRANK\\b', '\\bDENSE_RANK\\b', '\\bNTILE\\b',
            '\\bLAG\\b', '\\bLEAD\\b', '\\bFIRST_VALUE\\b', '\\bLAST_VALUE\\b'
        ]
        
        for func in functions:
            pattern = QRegExp(func, Qt.CaseInsensitive)
            self.highlighting_rules.append((pattern, function_format))
        
        # Strings (entre comillas simples)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(colors['string']))
        self.highlighting_rules.append((QRegExp("'[^']*'"), string_format))
        
        # Números
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(colors['number']))
        self.highlighting_rules.append((QRegExp("\\b[0-9]+\\.?[0-9]*\\b"), number_format))
        
        # Comentarios de línea (-- comentario)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(colors['comment']))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp("--[^\n]*"), comment_format))
        
        # Operadores
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(colors['operator']))
        operators = ['=', '!=', '<>', '<', '>', '<=', '>=', '\\+', '-', '\\*', '/', '%']
        for op in operators:
            self.highlighting_rules.append((QRegExp(op), operator_format))
    
    def highlightBlock(self, text):
        """Aplica el resaltado de sintaxis al bloque de texto"""
        for pattern, format_object in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format_object)
                index = expression.indexIn(text, index + length)


# Fix para import de Qt
try:
    from PyQt5.QtCore import Qt
except ImportError:
    pass
