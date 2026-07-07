# AgentHub 符号链接设置脚本
# 用于将各 Agent 工具的目录链接到 AgentHub 共享目录
#
# 使用方法：
#   .\setup-symlinks.ps1          # 创建所有符号链接
#   .\setup-symlinks.ps1 -Force   # 强制替换已存在的目录
#   .\setup-symlinks.ps1 -Remove  # 移除所有符号链接
#   .\setup-symlinks.ps1 -Sync    # 同步各工具的数据到共享目录

param(
    [switch]$Force,
    [switch]$Remove,
    [switch]$Sync
)

# 使用通用路径（不包含具体用户名）
$AgentHubRoot = Join-Path $env:USERPROFILE ".agenthub"

# 共享目录列表
$SharedDirs = @("skills", "agents", "profile", "memory", "config")

# 支持的工具及其目录映射
$Tools = @{
    "opencode" = @{
        "base" = Join-Path $env:USERPROFILE ".config\opencode"
        "links" = @("skills", "agents", "profile")
    }
    "cursor" = @{
        "base" = Join-Path $env:USERPROFILE ".cursor"
        "links" = @("skills", "agents")
    }
    "continue" = @{
        "base" = Join-Path $env:USERPROFILE ".continue"
        "links" = @("skills")
    }
}

function Write-Status {
    param([string]$Message, [string]$Status)
    
    switch ($Status) {
        "success" { Write-Host "[✓] $Message" -ForegroundColor Green }
        "error"   { Write-Host "[✗] $Message" -ForegroundColor Red }
        "info"    { Write-Host "[i] $Message" -ForegroundColor Yellow }
        "skip"    { Write-Host "[-] $Message" -ForegroundColor Gray }
    }
}

function Remove-Symlink {
    param([string]$Path)
    
    if (Test-Path $Path) {
        $item = Get-Item $Path -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            Remove-Item $Path -Force
            return $true
        }
    }
    return $false
}

function Create-Symlink {
    param([string]$Link, [string]$Target)
    
    # 确保目标目录存在
    if (-not (Test-Path $Target)) {
        New-Item -ItemType Directory -Path $Target -Force | Out-Null
    }
    
    # 创建符号链接
    try {
        New-Item -ItemType SymbolicLink -Path $Link -Target $Target -Force | Out-Null
        return $true
    } catch {
        Write-Host "错误: $_" -ForegroundColor Red
        return $false
    }
}

function Sync-Directory {
    param([string]$Source, [string]$Target)
    
    if (-not (Test-Path $Source)) {
        return 0
    }
    
    $count = 0
    $items = Get-ChildItem $Source -Directory
    
    foreach ($item in $items) {
        $targetPath = Join-Path $Target $item.Name
        
        if (-not (Test-Path $targetPath)) {
            Copy-Item $item.FullName $targetPath -Recurse -Force
            $count++
        }
    }
    
    return $count
}

function Ensure-SharedDirs {
    # 确保所有共享目录存在
    foreach ($dir in $SharedDirs) {
        $dirPath = Join-Path $AgentHubRoot $dir
        if (-not (Test-Path $dirPath)) {
            New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
            Write-Status "创建共享目录: $dir" "info"
        }
    }
}

# 主逻辑
Write-Host "AgentHub 符号链接设置" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# 确保共享目录存在
Ensure-SharedDirs

# 同步模式
if ($Sync) {
    Write-Host "同步模式：将各工具的数据同步到共享目录" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($tool in $Tools.GetEnumerator()) {
        $toolName = $tool.Key
        $toolConfig = $tool.Value
        $basePath = $toolConfig.base
        
        Write-Host "处理 $toolName ..." -ForegroundColor Yellow
        
        foreach ($dirName in $toolConfig.links) {
            $sourceDir = Join-Path $basePath $dirName
            $targetDir = Join-Path $AgentHubRoot $dirName
            
            if (Test-Path $sourceDir) {
                $item = Get-Item $sourceDir -Force
                
                # 跳过符号链接
                if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                    Write-Status "$toolName.$dirName 已是符号链接，跳过" "skip"
                    continue
                }
                
                # 同步数据
                $count = Sync-Directory $sourceDir $targetDir
                if ($count -gt 0) {
                    Write-Status "从 $toolName.$dirName 同步了 $count 个项目" "success"
                } else {
                    Write-Status "$toolName.$dirName 没有新数据需要同步" "skip"
                }
            }
        }
    }
    
    Write-Host ""
    Write-Host "同步完成！" -ForegroundColor Cyan
    return
}

# 创建/移除符号链接
foreach ($tool in $Tools.GetEnumerator()) {
    $toolName = $tool.Key
    $toolConfig = $tool.Value
    $basePath = $toolConfig.base
    
    Write-Host "处理 $toolName ..." -ForegroundColor Yellow
    
    foreach ($dirName in $toolConfig.links) {
        $linkPath = Join-Path $basePath $dirName
        $targetPath = Join-Path $AgentHubRoot $dirName
        
        # 移除模式
        if ($Remove) {
            if (Remove-Symlink $linkPath) {
                Write-Status "已移除 $toolName.$dirName 的符号链接" "success"
            } else {
                Write-Status "$toolName.$dirName 没有符号链接" "skip"
            }
            continue
        }
        
        # 检查是否已存在
        if (Test-Path $linkPath) {
            $item = Get-Item $linkPath -Force
            
            # 已经是符号链接
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                Write-Status "$toolName.$dirName 已链接" "skip"
                continue
            }
            
            # 是普通目录
            if (-not $Force) {
                Write-Status "$toolName.$dirName 已存在普通目录，使用 -Force 强制替换" "info"
                continue
            }
            
            # 备份原目录
            $backupPath = "$linkPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
            Rename-Item $linkPath $backupPath
            Write-Status "已备份 $toolName.$dirName 到 $backupPath" "info"
        }
        
        # 创建符号链接
        if (Create-Symlink $linkPath $targetPath) {
            Write-Status "已创建 $toolName.$dirName 的符号链接" "success"
        } else {
            Write-Status "创建 $toolName.$dirName 的符号链接失败" "error"
        }
    }
}

Write-Host ""
Write-Host "完成！" -ForegroundColor Cyan