param (
    [string]$Port = "6001",
    [string]$Message = "Xin chao FIT4012"
)

# Chỉnh sửa biến môi trường hiện tại
$env:RECEIVER_HOST="127.0.0.1"
$env:RECEIVER_PORT=$Port
$env:SOCKET_TIMEOUT="10"
$env:PYTHONUNBUFFERED="1"

Write-Host "Đang khởi động Receiver..." -ForegroundColor Cyan
$receiverProcess = Start-Process python -ArgumentList "receiver.py" -PassThru

Start-Sleep -Seconds 1

$env:SERVER_IP="127.0.0.1"
$env:SERVER_PORT=$Port
$env:MESSAGE=$Message

Write-Host "Đang khởi động Sender..." -ForegroundColor Cyan
python sender.py

# Dọn dẹp process khi chạy xong
if ($receiverProcess -and !$receiverProcess.HasExited) {
    Wait-Process -Id $receiverProcess.Id -Timeout 3 -ErrorAction SilentlyContinue
    if (!$receiverProcess.HasExited) {
        Stop-Process -Id $receiverProcess.Id -Force
    }
}
