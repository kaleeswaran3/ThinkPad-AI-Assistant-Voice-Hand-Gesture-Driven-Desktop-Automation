Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Check if virtual environment exists
venvPython = scriptDir & "\.venv\Scripts\python.exe"
guiScript = scriptDir & "\gui_assistant.py"

If fso.FileExists(venvPython) Then
    ' Use virtual environment Python
    WshShell.Run """" & venvPython & """ """ & guiScript & """", 0, False
ElseIf fso.FileExists(guiScript) Then
    ' Use system Python via py launcher
    WshShell.Run "py """ & guiScript & """", 0, False
Else
    MsgBox "Error: gui_assistant.py not found!", vbCritical, "ThinkPad Voice Assistant"
End If
