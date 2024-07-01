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

