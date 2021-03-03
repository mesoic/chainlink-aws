#!/bin/python

import modules.fluxMonitor as fm

if __name__ == "__main__": 

	Monitor = fm.fluxMonitor()
	Monitor.generate_env()
	Monitor.generate_keystore()