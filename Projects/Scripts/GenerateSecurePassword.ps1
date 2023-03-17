#Write the credentials in pop up message
$credential = Get-Credential

#Save a encrypted Password in file
$credential.Password | ConvertFrom-SecureString | Set-Content C:\Users\pcpc\Downloads\scriptsencrypted_passwordFinal.txt
