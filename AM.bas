Attribute VB_Name = "Module 1"
Sub AM()
'
' AM Macro
' Del , Remove Doublons Fais le min?
'
' Touche de raccourci du clavier: Ctrl+Shift+A
'
    I = 1
    While (Feuil1.Cells(I, 1) <> "")
        I = I + 1
    Wend
    Cells.Replace What:=",", Replacement:="", LookAt:=xlPart, SearchOrder:= _
        xlByRows, MatchCase:=False
    fin = "A1:I" + CStr(I - 1)
    Range(fin).Select
        
    fin = "$A$1:$I$" + CStr(I - 1)
    ActiveSheet.Range(fin).RemoveDuplicates Columns:=Array(1, 2, 3, 4, 5, 6, 7 _
        , 8, 9), Header:=xlYes
        
    I = 1
    While (Feuil1.Cells(I, 1) <> "")
        I = I + 1
    Wend
    
    Range("J2").Select
    ActiveCell.FormulaR1C1 = "=MIN(RC[-7]:RC[-1])"
    fin = "J2:J" + CStr(I - 1)
    Range("J2").Select
    Selection.AutoFill Destination:=Range(fin), Type:=xlFillDefault
    Range(fin).Select
    
End Sub

