document.getElementById('group-size').addEventListener('input', function () {
    if (this.value < 2) {
      this.setCustomValidity('Group size must be at least 2.');
    } else {
      this.setCustomValidity('');
    }
  });