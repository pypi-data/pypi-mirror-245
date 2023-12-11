from enum import Enum


class AttrType(Enum):
    DATA = 0
    FUNC = 1


# Recurse into these types and display every element when length < recurse_if_length_less_than
_iterate_types = (tuple, list, set, frozenset)
_dict_types = (dict,)
# Print the value of these types
_print_types = (int, float, str, bool, complex, type(None))

_junction = u"├"
_corner = u"└"
_hor = u"─"
_ver = u"│"
_arrow = u"→"

# List of attrs to display in `summarise`
# Each tuple is mutually exclusive, and searched in the given order
#  if a method is found, `summarise` attempts to call it with no arguments
# Each attr is a (string, type) pair indicating the attribute name and whether
#  it is expected to be data or a function
_attrs = [
    (
        ("shape", AttrType.DATA),
        ("__len__", AttrType.FUNC),
        ("qsize", AttrType.FUNC),
        ("length", AttrType.DATA),
    ),
    (("dtype", AttrType.DATA),),
    (("device", AttrType.DATA),),
]
_attr_name_map = {
    "__len__": "len"
}


def summarise(obj, display=False):
    """Returns or prints a one-line summary of `obj`."""
    s = ""
    if isinstance(obj, _print_types):
        s = f"{obj}: "
    cname = type(obj).__name__
    s = s + f"{cname}"
    found_attrs = []
    obj_attrs = dir(obj)
    for attr_grp in _attrs:
        for attr, attr_type in attr_grp:
            if attr in obj_attrs and callable(getattr(obj, attr)) == (attr_type == AttrType.FUNC):
                value = getattr(obj, attr)

                if callable(value):
                    try:
                        value = value()
                    except:
                        # if fails for any reason, skip
                        continue

                name = _attr_name_map.get(attr, attr)
                found_attrs.append(f"{name}={value}")
                break
    out = " ".join([s] + found_attrs)
    if display:
        print(out)
    else:
        return out


def _whatis(obj,
            rec_len_limit=4,
            unicode=True,
            hor_spacing=2,
            ver_spacing=1,
            show_index=False,
            display=True,
            is_value_in_dict=False,
            pad="",
            endpad="",
            is_last=False,
            fst=False,
            index=None,
            skip_top_pad=False,
            skip_btm_pad=False):
    """
    Internal function; see `whatis` below for missing docs.
    @param is_value_in_dict: Is this object a value in a dictionary?
    @param pad: String to left pad with. For '│ ├ set len=2', we would have pad='│ ' (note no '├').
    @param endpad: String to left pad with on the final line of this object e.g. pad='│ └'.
    @param is_last: Is this the last element in my parent's iterator?
    @param fst: Are we at depth=0 i.e. no parent obj?
    @param index: Index in parent iterator (or None for dicts).
    @param skip_top_pad: Iterators pad top/btm before printing - this removes top padding.
    @param skip_btm_pad: Iterators pad top/btm before printing - this removes bottom padding.
    @return:
    """
    rows = []

    def finish(row):
        if display:
            print(row)
        else:
            rows.append(row)
        return rows

    final_line_in_parent = is_last and not isinstance(obj, _iterate_types + _dict_types)

    ver = _ver if unicode else "|"
    junc = _junction if unicode else "-"
    corner = _corner if unicode else "L"
    arrow = _arrow if unicode else "->"
    key_start = _corner + _arrow if unicode else "->"

    summary = summarise(obj)

    if show_index and index is not None:
        summary = str(index) + f" {arrow} " + summary

    if fst:
        line = summary
    else:
        use_pad = endpad if final_line_in_parent else pad
        char = corner if final_line_in_parent else junc
        if is_value_in_dict:
            # line = [padding]│ └→ [summary]
            line = use_pad + char + " " + key_start + " " + summary
            # subsequent lines have additional padding
        else:
            # line = [padding]├ [summary]
            line = use_pad + char + " " + summary

    if isinstance(obj, _iterate_types + _dict_types):
        is_dict = isinstance(obj, _dict_types)

        if fst:
            newpad = newendpad = " " * hor_spacing
        else:
            newpad = pad + ver + " " * hor_spacing
            if is_last:
                newendpad = endpad + corner + " " * hor_spacing
            else:
                newendpad = endpad + ver + " " * hor_spacing

        if is_value_in_dict:
            newpad = newpad + " "*4
            newendpad = newendpad + " "*4

        if not skip_top_pad:
            for _ in range(ver_spacing):
                finish(pad + ver)
        finish(line)

        last_was_iterable = False

        length = len(obj)

        for ind, i in enumerate(obj):
            if ind >= rec_len_limit:
                break
            is_last = (ind == length - 1) and not is_dict
            out = _whatis(i,
                          pad=newpad,
                          endpad=newendpad if is_last else newpad,
                          is_last=is_last,
                          rec_len_limit=rec_len_limit,
                          index=None if is_dict else ind,
                          skip_top_pad=last_was_iterable or ind == 0 or is_dict,
                          skip_btm_pad=is_last or is_dict,
                          unicode=unicode,
                          hor_spacing=hor_spacing,
                          ver_spacing=ver_spacing,
                          show_index=show_index,
                          display=display,
                          )
            if not display:
                rows += out

            if is_dict:
                o = obj[i]
                is_last = (ind == length - 1)
                out = _whatis(o,
                              pad=newpad,
                              endpad=(newendpad if is_last else newpad),
                              is_last=is_last,
                              rec_len_limit=rec_len_limit,
                              index=None if is_dict else ind,
                              is_value_in_dict=True,
                              skip_top_pad=True,
                              skip_btm_pad=True,
                              unicode=unicode,
                              hor_spacing=hor_spacing,
                              ver_spacing=ver_spacing,
                              show_index=show_index,
                              display=display,
                              )
                if not display:
                    rows += out

                if not is_last:
                    finish(newpad + ver)

            last_was_iterable = isinstance(i, _iterate_types + _dict_types)

        # Too long, display '...' on new line
        if length > rec_len_limit:
            finish(newendpad + (_corner if unicode else "-") + " ...")

        if not skip_btm_pad:
            for _ in range(ver_spacing):
                finish(pad + ver)
    else:
        finish(line)

    if not display:
        return rows


def whatis(obj,
           rec_len_limit: int = 4,
           unicode: bool = True,
           hor_spacing: int = 2,
           ver_spacing: int = 1,
           show_index: bool = False,
           display: bool = True):
    """
    What is this object?
    @param obj: The object
    @param rec_len_limit: Do not look beyond this many elements in lists etc.
    @param unicode: Whether to use unicode characters.
    @param hor_spacing: Horizontal spacing (>=0).
    @param ver_spacing: Vertical spacing (>=0).
    @param show_index: Whether to show the index of each item in a list.
    @param display: If set to False, returns a list of lines rather than printing to stdout. Useful for testing mainly.
    """
    assert hor_spacing >= 0
    assert ver_spacing >= 0
    out = _whatis(obj,
                  rec_len_limit=rec_len_limit,
                  unicode=unicode,
                  hor_spacing=hor_spacing,
                  ver_spacing=ver_spacing,
                  show_index=show_index,
                  display=display,
                  fst=True,
                  skip_top_pad=True,
                  skip_btm_pad=True)
    if not display:
        return out
