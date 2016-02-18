from .models import db, InputItem, InputItemMetadata


def save_csv_to_db(raw_str, data, timestamp):
    input_item = InputItem(raw_string=raw_str, timestamp=timestamp)
    for datum in data:
        input_item.input_item_metadata.append(
            InputItemMetadata(name=datum[0], value=datum[1], type='text')
        )
        db.session.add(input_item)
    db.session.commit()


def save_txt_to_db(lines, timestamp):
    for line in lines:
        db.session.add(InputItem(raw_string=line, timestamp=timestamp))
    db.session.commit()