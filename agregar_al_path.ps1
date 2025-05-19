# agregar_al_path.ps1

# Obtener la ruta del script actual
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Obtener el PATH de usuario actual
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath.Split(';') -contains $projectPath) {
    Write-Output "La ruta ya está en el PATH."
} else {
    # Agregar la ruta al PATH
    $newPath = "$currentPath;$projectPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Output "La ruta $projectPath fue agregada al PATH de usuario."
    Write-Output "Cierra y vuelve a abrir la terminal para aplicar los cambios."
}