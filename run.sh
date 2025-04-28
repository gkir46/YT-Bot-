
#!/bin/bash
echo "بيسطب المتطلبات..."
pip install -r requirements.txt
nohup python bot.py > output.log 2>&1 &
echo "البوت شغال!"
