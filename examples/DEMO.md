# Demo: Governed Runtime in 60 seconds

## Clean run
```bash
python verify_events.py
python governor.py --cycles 5 --do-model
python verify_events.py
python rechain_events.py events.json events.fixed.json events.head
mv events.json events.pre_rechain.bak
mv events.fixed.json events.json
python verify_events.py
