import RPi.GPIO as GPIO
import time


flow_sensor_pin = 10
def setup_GPIO():
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(flow_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(flow_sensor_pin, GPIO.FALLING, callback=countPulse)
	
def clean_GPIO():
	GPIO.remove_event_detect(flow_sensor_pin)
	GPIO.cleanup()


def countPulse(channel):
	global pulse_count
	pulse_count += 1

pulse_count = 0
flow_rates = []

	
pulses_per_gallon = 462

try:
	setup_GPIO()
	while True:
		
		time.sleep(1)
		pulses = pulse_count
		pulse_count = 0
		gallons_per_second = pulses / pulses_per_gallon
		flow_rate_gpm = gallons_per_second * 60
			
		if flow_rate_gpm > 0:
			flow_rates.append(flow_rate_gpm)
			print(f"Current Flow Rate: {flow_rate_gpm:.2f} GPM")
except KeyboardInterrupt:
	pass
except Exception as e:
	print(f"An error occured: {e}")
finally:
	if flow_rates:
		average_flow_rate = sum(flow_rates) / len(flow_rates)
		print(f"Average Flow Rate: {average_flow_rate:.2f} GPM")

	else:
		print("\nNo flow rate data collection")

	clean_GPIO()