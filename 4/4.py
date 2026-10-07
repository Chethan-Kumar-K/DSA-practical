EMPTY = "EMPTY"
OCCUPIED = "OCCUPIED"
DELETED = "DELETED"

class HashTable:

    def __init__(self, size=11):
        self.size = size
        self.count = 0

        self.table = []

        for _ in range(size):
            self.table.append([EMPTY, None])

    def hash_function(self, pnr):
        return pnr % self.size

    def is_prime(self, number):

        if number < 2:
            return False

        if number == 2:
            return True

        if number % 2 == 0:
            return False

        divisor = 3

        while divisor * divisor <= number:

            if number % divisor == 0:
                return False

            divisor += 2

        return True

    def next_prime(self, number):

        while not self.is_prime(number):
            number += 1

        return number

    def load_factor(self):
        return self.count / self.size

    def validate_pnr(self, pnr):

        if not isinstance(pnr, int):
            print("Invalid PNR: PNR must be numeric.")
            return False

        if pnr < 0:
            print("Invalid PNR: PNR cannot be negative.")
            return False

        if len(str(pnr)) != 10:
            print("Invalid PNR: PNR must contain exactly 10 digits.")
            return False

        return True

    def display(self):

        print("\n" + "=" * 10)
        print("HASH TABLE")
        print("=" * 10)

        print(
            f"{'Index':<8}"
            f"{'State':<12}"
            f"{'PNR':<15}"
            f"{'Passenger':<22}"
            f"{'Train':<10}"
            f"{'Status':<15}"
        )

        print("-" * 10)

        for i in range(self.size):

            state = self.table[i][0]
            record = self.table[i][1]

            if state == EMPTY:

                print(
                    f"{i:<8}"
                    f"{'EMPTY':<12}"
                    f"{'-':<15}"
                    f"{'-':<22}"
                    f"{'-':<10}"
                    f"{'-':<15}"
                )

            elif state == DELETED:

                print(
                    f"{i:<8}"
                    f"{'DELETED':<12}"
                    f"{'-':<15}"
                    f"{'-':<22}"
                    f"{'-':<10}"
                    f"{'-':<15}"
                )

            else:

                print(
                    f"{i:<8}"
                    f"{'OCCUPIED':<12}"
                    f"{record[0]:<15}"
                    f"{record[1]:<22}"
                    f"{record[2]:<10}"
                    f"{record[3]:<15}"
                )

        print("-" * 95)

        print(
            f"Occupied = {self.count} | "
            f"Table Size = {self.size} | "
            f"Load Factor = {self.load_factor():.3f}"
        )

        print("=" * 10)

    def search(self, pnr):

        if self.count == 0:
            print("Table is empty")
            return None

        if not self.validate_pnr(pnr):
            return None

        home_index = self.hash_function(pnr)
        probes = 0

        for i in range(self.size):

            index = (home_index + i) % self.size
            probes += 1

            state = self.table[index][0]

            if state == EMPTY:

                print(
                    f"PNR not found. Probes = {probes}"
                )

                return None

            if state == OCCUPIED:

                record = self.table[index][1]

                if record[0] == pnr:

                    print("\nPNR FOUND")
                    print("-" * 40)
                    print(f"PNR       : {record[0]}")
                    print(f"Passenger : {record[1]}")
                    print(f"Train No. : {record[2]}")
                    print(f"Status    : {record[3]}")
                    print(f"Index     : {index}")
                    print(f"Probes    : {probes}")

                    return record
                
        print(
            f"PNR not found. Probes = {probes}"
        )

        return None

    def insert(self, record, allow_rehash=True):

        pnr = record[0]

        if not self.validate_pnr(pnr):
            return False

        home_index = self.hash_function(pnr)

        first_deleted = -1
        probes = 0

        for i in range(self.size):

            index = (home_index + i) % self.size
            probes += 1

            state = self.table[index][0]

            if state == EMPTY:

                if first_deleted != -1:
                    final_index = first_deleted
                else:
                    final_index = index

                self.table[final_index][0] = OCCUPIED
                self.table[final_index][1] = record

                self.count += 1

                print("\nINSERT SUCCESSFUL")
                print(f"PNR         : {pnr}")
                print(f"Home Index  : {home_index}")
                print(f"Final Index : {final_index}")
                print(f"Probes      : {probes}")

                if allow_rehash and self.load_factor() > 0.7:

                    print("\nLoad factor exceeded 0.7.")
                    self.rehash()

                return True

            elif state == OCCUPIED:

                existing_record = self.table[index][1]

                if existing_record[0] == pnr:

                    print("\nDuplicate PNR")
                    print("Insertion rejected.")

                    return False

            elif state == DELETED:

                if first_deleted == -1:
                    first_deleted = index

        if first_deleted != -1:

            self.table[first_deleted][0] = OCCUPIED
            self.table[first_deleted][1] = record

            self.count += 1

            print("\nINSERT SUCCESSFUL")
            print(f"PNR         : {pnr}")
            print(f"Home Index  : {home_index}")
            print(f"Final Index : {first_deleted}")
            print(f"Probes      : {probes}")
            print("DELETED slot was reused.")

            if allow_rehash and self.load_factor() > 0.7:
                self.rehash()

            return True

        print("\nHash table overflow.")
        return False

    def delete(self, pnr):

        if self.count == 0:
            print("Table is empty")
            return False

        if not self.validate_pnr(pnr):
            return False

        home_index = self.hash_function(pnr)
        probes = 0

        for i in range(self.size):

            index = (home_index + i) % self.size
            probes += 1

            state = self.table[index][0]

            if state == EMPTY:

                print("PNR not found")
                return False

            if state == OCCUPIED:

                record = self.table[index][1]

                if record[0] == pnr:

                    self.table[index][0] = DELETED
                    self.table[index][1] = None

                    self.count -= 1

                    print("\nDELETE SUCCESSFUL")
                    print(f"PNR          : {pnr}")
                    print(f"Deleted Index: {index}")
                    print(f"Probes       : {probes}")

                    return True

        print("PNR not found")
        return False

    def rehash(self):

        old_size = self.size

        print("\n" + "#" * 10)
        print("REHASHING STARTED")
        print("#" * 10)

        print("\nTABLE BEFORE REHASHING:")
        self.display()

        new_size = self.next_prime(2 * old_size)

        print(f"\nOld table size : {old_size}")
        print(f"New table size : {new_size}")

        records = []

        for i in range(old_size):

            if self.table[i][0] == OCCUPIED:
                records.append(self.table[i][1])

        self.size = new_size
        self.count = 0

        self.table = []

        for _ in range(self.size):
            self.table.append([EMPTY, None])

        for record in records:
            self.insert(record, allow_rehash=False)

        print("\nTABLE AFTER REHASHING:")
        self.display()

        print("#" * 10)
        print("REHASHING COMPLETED")
        print("#" * 10)

bookings = [

    [8203416572, "Ananya Rao", 12627, "CONFIRMED"],

    [8203416583, "Rahul Menon", 12627, "RAC"],

    [8203416540, "Fatima Sheikh", 16526, "CONFIRMED"],

    [8203416599, "Vikram Iyer", 12008, "WAITLIST"],

    [8203416615, "Divya Nair", 12627, "CONFIRMED"],

    [8203416561, "Arjun Patil", 16526, "RAC"],

    [8203416604, "Sneha Kulkarni", 12008, "CONFIRMED"],

    [8203416626, "Karthik Gowda", 12627, "WAITLIST"]
]

def demonstration():

    ht = HashTable()

    print("\n")
    print("=" * 10)
    print("RAILSWIFT - TASK 5 DEMONSTRATION")
    print("=" * 10)

    for i in range(7):

        print("\n")
        print("-" * 10)
        print(f"INSERTION #{i + 1}")
        print("-" * 10)

        ht.insert(bookings[i])

    print("\n")
    print("=" * 10)
    print("TASK 5.1 - TABLE AFTER INSERTION #7")
    print("=" * 10)

    ht.display()

    print("\n")
    print("=" * 10)
    print("TASK 5.2 - DELETE RAHUL MENON")
    print("=" * 10)

    ht.delete(8203416583)

    ht.display()

    print("\n")
    print("=" * 10)
    print("TASK 5.3 - SEARCH ARJUN PATIL")
    print("=" * 10)

    ht.search(8203416561)

    print("\n")
    print("=" * 10)
    print("TASK 5.4 - SEARCH DELETED RAHUL MENON")
    print("=" * 10)

    ht.search(8203416583)

    print("\n")
    print("=" * 10)
    print("TASK 5.5 - INSERT Karthik Gowda")
    print("=" * 10)

    ht.insert(bookings[7])

    ht.display()

    print("\n")
    print("=" * 10)
    print("TASK 5 COMPLETED")
    print("=" * 10)

if __name__ == "__main__":
    demonstration()