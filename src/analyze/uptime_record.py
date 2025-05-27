from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from pathlib import Path
from enum import Enum

class WeekDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

@dataclass
class UptimeRecord:
    end_time: datetime
    duration: timedelta

    @property
    def start_time(self) -> datetime:
        return self.end_time - self.duration

    @staticmethod
    def parse_line(line: str) -> "UptimeRecord":
        pattern = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+-\s+(\d+):(\d{2})$"
        match = re.match(pattern, line.strip())
        if not match:
            raise ValueError(f"Invalid line format: {line}")

        end_str, hours, minutes = match.groups()
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
        duration = timedelta(hours=int(hours), minutes=int(minutes))
        return UptimeRecord(end_time=end_time, duration=duration)

    @staticmethod
    def parse_file(filepath: str) -> list["UptimeRecord"]:
        records = []
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    record = UptimeRecord.parse_line(line)
                    records.append(record)
        return records

    @staticmethod
    def parse_folder(folder_path: str) -> list["UptimeRecord"]:
        all_records = []
        for txt_file in Path(folder_path).glob("*.txt"):
            all_records.extend(UptimeRecord.parse_file(str(txt_file)))
        return all_records

    @staticmethod
    def fuse(records: list["UptimeRecord"], tolerance: timedelta = timedelta(minutes=1)) -> list["UptimeRecord"]:
        if not records:
            return []

        sorted_records = sorted(records, key=lambda r: r.start_time)
        fused = [sorted_records[0]]

        for record in sorted_records[1:]:
            last = fused[-1]
            if record.start_time <= last.end_time + tolerance:
                new_end = max(last.end_time, record.end_time)
                new_start = min(last.start_time, record.start_time)
                fused[-1] = UptimeRecord(
                    end_time=new_end,
                    duration=new_end - new_start
                )
            else:
                fused.append(record)

        return fused

    def uptime_by_day(self) -> list[tuple[WeekDay, timedelta]]:
        daily_uptime = {day: timedelta(0) for day in WeekDay}

        current_start = self.start_time
        current_end = self.end_time

        while current_start < current_end:
            # Start of next day
            next_day = (current_start + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            split_end = min(current_end, next_day)
            duration = split_end - current_start

            weekday = WeekDay(current_start.weekday())
            daily_uptime[weekday] += duration

            current_start = split_end

        return [(day, daily_uptime[day]) for day in WeekDay if daily_uptime[day] > timedelta(0)]

# === TEST CASES ===
def _test_fusion():
    now = datetime.now()
    records = [
        UptimeRecord(end_time=now, duration=timedelta(minutes=10)),
        UptimeRecord(end_time=now + timedelta(minutes=1), duration=timedelta(minutes=5)),  # within 1 min
        UptimeRecord(end_time=now + timedelta(minutes=20), duration=timedelta(minutes=5))  # separate
    ]
    fused = UptimeRecord.fuse(records)
    for rec in fused:
        print(f"Start: {rec.start_time}, End: {rec.end_time}, Duration: {rec.duration}")

    print("\nUptime by day:")
    for rec in fused:
        daily = rec.uptime_by_day()
        for day, dur in daily:
            print(f"{day.name}: {dur}")

def _test_uptime_by_day():
    # Record spans across two days: from Monday 23:30 to Tuesday 01:30
    start = datetime(2024, 5, 6, 23, 30)  # Monday
    end = datetime(2024, 5, 7, 1, 30)     # Tuesday
    record = UptimeRecord(end_time=end, duration=end - start)

    results = dict(record.uptime_by_day())
    assert WeekDay.MONDAY in results
    assert WeekDay.TUESDAY in results

    # Monday has 30 minutes, Tuesday has 1 hour 30 minutes
    assert results[WeekDay.MONDAY] == timedelta(minutes=30), f"Expected 30m, got {results[WeekDay.MONDAY]}"
    assert results[WeekDay.TUESDAY] == timedelta(hours=1, minutes=30), f"Expected 1h30m, got {results[WeekDay.TUESDAY]}"
    
    print("✓ _test_uptime_by_day passed.")

if __name__ == "__main__":
    _test_fusion()
    _test_uptime_by_day()