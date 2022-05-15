climate = input('enter the climate and press Return: ')
if climate == 'Tropical': thresh = 30.0
elif climate == 'Continental': thresh = 25.0
else: thresh = 18.0
#print(thresh)
#print(type(thresh))
#print(climate + ' climate')
samples = eval(input('enter the temperature data as a list and press Return: '))
#print(type(samples))
#print(type(samples[0]))
n = len(samples)
for i in range(0, n):
    if float(samples[i]) <= thresh: 
        print('F')
    elif float(samples[i]) > thresh: 
        print('U')
#print('The expected behavior of the plant leaves was listed for each temperature. U = unfolded; F = folded')
#Done