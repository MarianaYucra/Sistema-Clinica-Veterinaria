import pytest
from unittest.mock import patch
from app.main import main

def test_keyboard_interrupt_at_main_menu(capsys):
    """Prueba que KeyboardInterrupt en el menú principal cierre el programa limpiamente."""
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        main()
    
    captured = capsys.readouterr()
    assert "¡Hasta luego!" in captured.out


def test_keyboard_interrupt_inside_action(capsys):
    """Prueba que KeyboardInterrupt dentro de una acción (ej. Registrar Cliente) la cancele y vuelva al menú."""
    # Simula ingresar la opción 1 (Registrar Cliente), luego presionar Ctrl+C en el primer input de la acción, y finalmente opción 0 para salir.
    with patch("builtins.input", side_effect=["1", KeyboardInterrupt(), "0"]):
        main()
        
    captured = capsys.readouterr()
    assert "[Operación cancelada por el usuario]" in captured.out
    assert "¡Hasta luego!" in captured.out
