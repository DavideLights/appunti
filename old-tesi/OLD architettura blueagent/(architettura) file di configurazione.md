# yaml
> descrive una patch challenge

```yaml
name: challenge-example
description: descrizione

verify-internet-access: true

containers:
	database:
		ip: 1
		cpu limits: 1
		ram imits: 512MB
	server:
		ip: 2
		cpu limits: 2
		ram limits: 512MB
	verifier:
		ip: 100
		cpu limits: 2
		ram limits: 512MB

readyness-steps:
	name: verify server running
	incus-exec: echo "hello world!"
	container: server
	starts-with:
	contains: hello
	ends-with: 
	timeout: 10

verify-steps:
- name: exec payload
  incus-exec: echo "verified"
  contianer: verifier
  
  starts-with:
  contains: verified
  ends-with: 
  
  timeout: 10

```