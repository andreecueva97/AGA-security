#Si has configurado tu servidor SMTP en el puerto 465 (con SSL) y en el puerto 587 (con TLS) pero 
#sigues teniendo problemas para enviar correo, 
#prueba a configurar tu SMTP para que utilice el puerto 25 (con SSL).
$From = "aaaa6@hotmail.com"
$To = "aaaaaa16@hotmail.com"
$Cc = "aaaaaa_16@hotmail.com"
$Attachment = "C:\Users\pcpc\Desktop\506.txt"
$Subject = "data csv ad"
$Body = "<h2>download csv data ad!</h2><br><br>"
$Body += "bye"
$SMTPServer = "smtp.office365.com"
$SMTPPort = "587"
Send-MailMessage -From $From -to $To -Cc $Cc -Subject $Subject -Body $Body -BodyAsHtml -SmtpServer $SMTPServer -Port $SMTPPort -UseSsl -Credential (Get-Credential) -Attachments $Attachment
