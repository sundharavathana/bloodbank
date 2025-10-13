document.getElementById('donateModal').addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const patientId = button.getAttribute('data-patient-id');
  const patientName = button.getAttribute('data-patient-name');

  document.getElementById('modalPatientId').value = patientId || '';
  document.getElementById('modalPatientName').textContent = patientName || 'patient';
});