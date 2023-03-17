#Site collection URL
$SiteURL = "https://ucao365.sharepoint.com/sites/MisDocumentos"
 
#Connect to SharePoint Online with ClientId and ClientSecret
Connect-PnPOnline -Url $SiteURL -ClientId "a541............87e9" -ClientSecret "Uxih/.....="
 
#Get-PnPContext
#------------------------
$URL ="https://ucao365.sharepoint.com/sites/MisDocumentos"
$ErrorActionPreference = "Stop"
$PSDefaultParameterValues["*:ErrorAction"]="Stop"

#$emailusername = "adfasdsu2@fdsadasdsfar"
#$encrypted = Get-Content C:\Users\pcpc\Downloads\scriptsencrypted_password1.txt | ConvertTo-SecureString
#$credential = New-Object System.Management.Automation.PsCredential($emailusername,$encrypted)

Import-Module SharePointPnPPowerShellOnline
#Connect-PnPOnline -Url $URL -Credentials $credential
#Get-PnPFile -Url $SiteURL
$Files = Get-ChildItem "C:\Users\pcpc\Desktop\AA"
foreach($File in $Files){
    Add-PnPFile -Folder "Documentos Compartidos" -Path $File.FullName

}
