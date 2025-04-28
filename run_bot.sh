
#!/bin/bash

SESSION_NAME="youtube_bot"

tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  echo "بيعمل جلسة جديدة باسم $SESSION_NAME..."
  tmux new-session -d -s $SESSION_NAME "python bot.py"
else
  echo "الجلسة موجودة، بيشغل البوت..."
fi

tmux attach-session -t $SESSION_NAME
