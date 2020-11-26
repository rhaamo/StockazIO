def join_url(start, end):
    if end.startswith("http://") or end.startswith("https://"):
        # alread a full URL, joining makes no sense
        return end
    if start.endswith("/") and end.startswith("/"):
        return start + end[1:]

    if not start.endswith("/") and not end.startswith("/"):
        return start + "/" + end

    return start + end
