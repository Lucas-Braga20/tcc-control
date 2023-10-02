from bs4.element import Tag


def get_sub_items(item):
    """Recursive Function to get sub-items or item of type bs4.element.Tag."""

    is_tag = isinstance(item, Tag)

    if is_tag:
        has_childrens = len(list(item.children)) > 1
        attributes = dict(item.attrs)
        if 'class' in attributes:
            classes = attributes['class']
            # Concatena as classes em uma única string
            classes_concatenadas = " ".join(classes)
        else:
            classes_concatenadas = ""
        for sub_item in item.children:
            if sub_item != '\n' and isinstance(item, Tag):
                has_childrens = True

        if has_childrens:
            return [
                {
                    "tag_name": sub_item.name,
                    "attributes": dict(sub_item.attrs),
                    "classes": classes_concatenadas,
                    "values": get_sub_items(sub_item)
                } if isinstance(sub_item, Tag) else sub_item
                for sub_item in item.children if sub_item != "\n"
            ]

        # Recursive function stopping condition
        # When the element is a tag with no descendants
        return item.text

    return [{"tag_name": sub_item.name, "values": get_sub_items(sub_item), "classes": " ".join(dict(sub_item.attrs)['class']) if 'class' in dict(sub_item.attrs) else ""}
            for sub_item in item if sub_item != '\n']