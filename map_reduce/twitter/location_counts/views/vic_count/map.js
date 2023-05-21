function(doc) {
    if (doc.state && doc.state.includes('Victoria')) {emit(doc.location, 1);}
}