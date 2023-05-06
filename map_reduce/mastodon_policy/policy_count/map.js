function (doc) {
  if (doc.political_related == true) {
    emit(doc._id, 1);
  }
}