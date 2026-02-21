from wal import WAL

wal = WAL("wal.log")

seq = wal.append({"action": "add_memory", "content": "engineer"})
print("Appended seq:", seq)

wal.mark_committed(seq)
print("Marked committed.")

print("WAL contents:")
for entry in wal.read_all():
    print(entry)
