document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.clickable').forEach(function(tr) {
    tr.onclick = function () {
      const url = '/samples/' + this.dataset.sample_no;
      window.location.href = url;
    }
  });
});
