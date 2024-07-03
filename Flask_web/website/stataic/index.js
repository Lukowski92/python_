function delete_note(patinetId) {
    fetch("/delete-note", {
            method: "POST",
            body: JSON.stringify({ patinetId: patinetId}),
        }).then((_res)=>{
            window.location.href="/";
        });
}

function doThing(event) {
    event.preventDefault();
    window.confirm('Do you want to do?') ? 
      window.location.href = '/deletePatient' :
      null;
  };


  function selectPatient(event) {
    const patientIdInput = document.getElementById('patient_id');
    const selectedPatient = Array.from(document.querySelectorAll('#patientList option')).find(
        option => option.value === event.target.value.trim()
    );

    if (selectedPatient) {
        patientIdInput.value = selectedPatient.dataset.id;
    } else {
        patientIdInput.value = '';
    }
}
