# type: ignore
import csv
import sys

import matplotlib.pyplot as plt
import pyhtml as ht

css = ht.style("""
    table, th, td {
        border:1px solid black;
    }
""")

student_details = ht.html(
    ht.head(ht.title("Student Data"), css),
    ht.body(
        ht.h1("Student Details"),
        ht.table(
            ht.tr(ht.th("Student ID"), ht.th("Course ID"), ht.th("Marks")),
            lambda ctx: [ht.tr([ht.td(j) for j in i]) for i in ctx.get("records", [])],
            ht.tr(
                ht.td(colspan=2)("Total Marks"),
                ht.td(lambda ctx: sum([int(i[2]) for i in ctx.get("records", [])])),
            ),
        ),
    ),
)

course_data = ht.html(
    ht.head(ht.title("Course Data"), css),
    ht.body(
        ht.h1("Course Details"),
        ht.table(
            ht.tr(ht.th("Average Marks"), ht.th("Maximum Marks")),
            ht.tr(
                lambda ctx: [
                    ht.td(ctx.get("avg_marks", 0)),
                    ht.td(ctx.get("max_marks", 0)),
                ]
            ),
        ),
        ht.img(src="./graph.png", alt="Histogram"),
    ),
)

invalid = ht.html(
    ht.head(ht.title("Something went wrong")),
    ht.body(ht.h1("Wrong Inputs"), ht.p("Something went wrong")),
)


def main():
    try:
        if sys.argv[1].lower() == "-s":
            student_id = sys.argv[2]

            data_file = csv.reader(open("data.csv", newline=""))
            records = [row for row in data_file if row[0].strip() == student_id]

            if records:
                output = student_details.render(records=records)
                with open("output.html", "w") as f:
                    f.write(output)
            else:
                raise Exception("Records is empty.")
        elif sys.argv[1].lower() == "-c":
            course_id = sys.argv[2]
            data_file = csv.reader(open("data.csv", newline=""))
            records = [int(row[2]) for row in data_file if row[1].strip() == course_id]

            if records:
                avg_marks = sum(records) / len(records)
                max_marks = max(records)

                plt.hist(records)
                plt.xlabel("Marks")
                plt.ylabel("Frequency")
                plt.savefig("graph.png")

                output = course_data.render(avg_marks=avg_marks, max_marks=max_marks)
                with open("output.html", "w") as f:
                    f.write(output)
            else:
                raise Exception("Records is empty.")

        else:
            raise Exception("No flag provided.")
    except Exception as e:
        print(e)
        output = invalid.render()
        with open("output.html", "w") as f:
            f.write(output)


if __name__ == "__main__":
    main()
