$URL ="https://ucao365.sharepoint.com/sites/DSAFSDAFSAF"
$ErrorActionPreference = "Stop"
$PSDefaultParameterValues["*:ErrorAction"]="Stop"

$emailusername = "AFDASFFDS@uFADSFDFSAF"
$encrypted = Get-Content C:\Users\pcpc\Downloads\scriptsencrypted_password1.txt | ConvertTo-SecureString
$credential = New-Object System.Management.Automation.PsCredential($emailusername,$encrypted)

#Use line 10, if you use SharePointPnPPowerShellOnline MODULE, but you use PnPPowerShell not need that
#Import-Module SharePointPnPPowerShellOnline
Connect-PnPOnline -Url $URL -Credentials $credential
$Files = Get-ChildItem "C:\Users\pcpc\Desktop\AA"
foreach($File in $Files){
    Add-PnPFile -Folder "Documentos Compartidos" -Path $File.FullName
    #Remove-Item -Path $File.FullName
    #Move-Item -Path $File.FullName -Destination "dfasfdadfafds/fadsffd/sfadfadsfs/eewrewr/dfasf"
}
