#Date
$Date = Get-Date -UFormat "%YYYY%mm%dd"

#Name file to create
$FilenameUsers = "C:\Users\pcpc\Dekstop\AD_Users\AD_Users_"+$Date+".csv"

#Delete Old Files in this path
$FileUsersList = Get-Children "C:\Users\pcpc\Dekstop\AD_Users"
Remove-Item -Path $FileUsersList -Recurse

#Get Data from ACTIVE DIRECTORY by OU or DC
Get-ADUser -SearchBar "OU=Name1, OU=Name8, DC=DC01, DC=local" -filter * -Properties * |  Export-csv -Path $FilenameUsers -NoTypeInformation

#Get Data from ACTIVE DIRECTORY
Get-ADUser -filter * -Properties * |  Export-csv -Path $FilenameUsers -NoTypeInformation

#Get Data Computers from ACTIVE DIRECTORY
#Similar, you need use --> Get-ADComputer ....
