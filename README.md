# taskweb

Need to save 

```
[Unit]
Description=Minimal Taskwarrior Web Server
After=network.target

[Service]
User=harry
WorkingDirectory=/home/harry
ExecStart=/usr/bin/python3 /home/harry/taskweb/tasks.py
Restart=always

[Install]
WantedBy=multi-user.target
```

in 

`/etc/systemd/system/todo.service`

and run 

```
sudo systemctl daemon-reload
sudo systemctl enable todo.service
sudo systemctl start todo.service
```

on initial set up or 

```
sudo systemctl restart todo.service
```

when I make changes.
