## Deptos Scraper

Credit for the original idea goes to the following article: https://dev.to/fernandezpablo/scrappeando-propiedades-con-python-4cp8. This is mainly a rewrite.

Example crontab por scheduling:
```
# Run every 5th minute
*/5 * * * * ec2-user /home/ec2-user/app/run.sh &>> /tmp/cron_errors.log
```

Example script for running:
```bash
#!/bin/bash
python3 /home/ec2-user/app/main.py --config /home/ec2-user/app/Config.json --log /home/ec2-user/app/app.log
```

### TODO
- [X] Add a CLI to input the configuration file path and log file
- [ ] Add a configuration to select a dummy notifier
- [ ] Support pagination