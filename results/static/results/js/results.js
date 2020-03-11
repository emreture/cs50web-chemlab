document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.clickable').forEach(function(tr) {
    tr.onclick = function () {
      const url = '/results/' + this.dataset.sample_no;
      window.location.href = url;
    }
  });
});
