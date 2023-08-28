Attribute VB_Name = "Module 11"
Sub flight()

I = 1
While (Feuil1.Cells(I, 1) <> "")
    I = I + 1
Wend

Cells.Replace What:=",", Replacement:="", LookAt:=xlPart, SearchOrder:= _
        xlByRows, MatchCase:=False
Cells.Replace What:="$", Replacement:="", LookAt:=xlPart, SearchOrder:= _
        xlByRows, MatchCase:=False
choix = "F2:F" + CStr(I)
Range(choix).Select
    Selection.NumberFormat = "0.00"

Range("H2").Select
ActiveCell.FormulaR1C1 = "=IF(RC[-1]<0,1,0)"
    fin = "H2:H" + CStr(I - 1)
    Selection.AutoFill Destination:=Range(fin), Type:=xlFillDefault
    Range("H2").Select

j = 1
For tes = 2 To I
If (Feuil1.Cells(tes, 8) = 1) Then
    choix = "A" + CStr(tes) + ":" + "G" + CStr(tes)
        Range(choix).Select
        Range(choix).Copy
        Cells(j, 11).Select
            ActiveSheet.Paste
        j = j + 1
End If

Next

End Sub
Sub Macro1()
Attribute Macro1.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Macro1 Macro
'

'
    Range("H2").Select
    Selection.AutoFill Destination:=Range("H2:H17"), Type:=xlFillDefault
    Range("H2:H17").Select
End Sub
