from models.CSV_Reader import Delivery, reset

sim = Delivery()
sim.run("16:47")

print("Name: Alyssa Weiglein")
print("Student ID: #001104678")
print("\nWGUPS TRACKING SYSTEM")
print('Route completed in', "{0:.2f}".format(sim.total_distance(), 2), 'miles.')

while True:
    print("\nMAIN MENU -------------------")
    print("| 1 | Package Lookup")
    print("| 2 | Check Delivery Status")
    print("-----------------------------")
    selected = input("Enter 1 or 2: ")

    # user looks up package by id
    if selected == '1':
        reset()
        sim.run(input("\nPackage Lookup\n-----------------------------\nEnter time in 'HH:MM' format: "))
        sim.print(int(input("Enter package ID (1-40): ")))

    # user checks delivery status of all packages
    if selected == '2':
        reset()
        sim.run(input("\nCheck Delivery Status\n-----------------------------\nEnter time in 'HH:MM' format: "))
        sim.print()