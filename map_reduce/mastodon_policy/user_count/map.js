function (doc) {
  if (doc.political_related == true) {
    emit(doc.username, 1);
  }
}