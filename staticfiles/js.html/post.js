window.onload = function() {
    const study_subjects = [
        "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
        "English", "History", "Geography", "Economics", "Political Science",
        // Add more subjects here
    ];

    function attachAutoComplete(input_box_id, result_box_class) {
        const input_box = document.getElementById(input_box_id);
        const result_box = document.querySelector(result_box_class);

        input_box.onkeyup = function() {
            let result = [];
            let input = input_box.value;
            if (input.length) {
                result = study_subjects.filter((keyword) => {
                    return keyword.toLowerCase().includes(input.toLowerCase());
                });
            }
            display(result, result_box);
        };

        function display(result, result_box) {
            const content = result.map((list) => {
                return `<li onclick="selectItem('${input_box_id}', '${result_box_class}', this)">${list}</li>`;
            });
            result_box.innerHTML = `<ul>${content.join('')}</ul>`;
        }
    }

    attachAutoComplete("box", ".res_box");
    attachAutoComplete("two_box", ".two_res_box");
    attachAutoComplete("three_box", ".three_res_box");
};

function selectItem(input_box_id, result_box_class, list) {
    const input_box = document.getElementById(input_box_id);
    input_box.value = list.innerHTML;
    document.querySelector(result_box_class).innerHTML = '';
}
