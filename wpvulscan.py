import subprocess



def wpscan(url):
	command = ['sudo', 'docker', 'run', '-it', '--rm', 'wpscanteam/wpscan', '-u', url, '--user-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', '--no-banner']
	output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
	return output


def main():
	url = input('[*] Enter the URL: ')
	result = wpscan(url)
	print()
	print()
	print(result)



if __name__=='__main__':
	main()
