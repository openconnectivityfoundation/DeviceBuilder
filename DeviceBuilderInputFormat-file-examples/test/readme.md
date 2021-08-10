# info

## test_1

Fake device includes:

- light
   - oic.r.switch.binary
   - oic.r.light.dimming
   - oic.r.colour.chroma
- module testing
   - oic.r.test.variant
   - oic.r.test.query
   - oic.r.test.range
- thermostat
   - oic.r.temperature

Testing :
- boolean
- integer
- number
- string
- range
- query param


## test_2

fake device
- oic.r.airquality
- oic.r.alarm
- oic.r.audio
- oic.r.energy.battery
- oic.r.automaticdocumentfeeder
- oic.r.location.civic


Testing :
- time (alarm)
- range (audio)
- partial update (difference in GET and POST) energy battery
- if rw, 
