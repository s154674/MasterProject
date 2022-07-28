import matplotlib.pyplot as plt

All = 3706375
Main= 632742
Arbi= 386421
Opti= 1242960
Poly= 1444252

# without router addresses
All = 3706375
Main2= 343182
Arbi2= 94714
Opti2= 556892
Poly2= 547276

All2 = Main2 + Arbi2 + Opti2 + Poly2


labels = 'Mainnet', 'Arbitrum', 'Optimism', 'Polygon PoS'
sizes = [632742,386421,1242960,1444252]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True,)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(['Mainnet: 632742', 'Arbitrum: 386421', 'Optimism: 1242960', 'Polygon Pos: 1444252', 'Total: '])
plt.show()
plt.close()

print(Main2/Main)
print(Arbi2/Arbi)
print(Opti2/Opti)
print(Poly2/Poly)
print(All2/All)

print(All2)



networks = ['Arbitrum', 'Optimism', 'Polygon PoS','Mainnet']
distinct_addresses = [44,55,165,294]


fig = plt.figure(figsize = (8, 5))
 
# creating the bar plot
plt.bar(networks, distinct_addresses, color ='steelblue',
        width = 0.4)
 
plt.xlabel("Network")
plt.ylabel('# Distinct Sender Addresses')
# plt.title("Students enrolled in different courses")
plt.show()