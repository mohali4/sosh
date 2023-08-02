SERVICE="""
[Unit]
Description=sosh node :) 
After=network.target auditd.service

[Service]
Type=simple
User=root
WorkingDirectory={workingDir}
ExecStart={execStart}

[Install]
WantedBy=multi-user.target
"""