let limit = 15

sort.sort_up = false
sort.current_parameter = 'date'
sort.previous_parameter = ''
$("#" + sort.current_parameter).attr("data-order", "1")


th.classList.add("th-grade")

function show_more(new_field, user_id) {

    limit += new_field

    $.post('/show_more_grades_for_user', {
        lim: limit,
        parameter: sort.current_parameter,
        sort_up: sort.sort_up,
        user_id: user_id
    }).done(function (response) {

        //$("#tbody").html('')
        $('#tbody tr').each(function (index, element) {
            if (index !== 0) {
                $(element).remove()
            }
        })

        let grades = JSON.parse(response['grades'])
        let quantity = grades.length

        if (limit > quantity) {
            quantity < 15 ? limit = 15 : limit = quantity
            $('body').append(
                `<div class="message warning"><h4>
                В таблице присутствуют все оценки участника</h4></div>`)
            setTimeout( ()=> {
                $('.message').css({transition: 'all 0.3s ease', opacity: 0})}, 4000)
            setTimeout( ()=> {
                $('.message').css({display: 'none'})}, 4100)
            $('#show_more').css('display', 'none')
            $('#show_all').css('display', 'none')
        }
        else {
            $('#show_more').css('display', 'inline-block')
            $('#show_all').css('display', 'inline-block')
        }

        for (let i = 0; i < quantity; i++) {
            let k
            i === 0 ? k = 1 : k = i + 1
            console.log(k, i)
            $("#tbody").append(`<tr id="number_str${k}"></tr>`)

            if (grades[i]['date'] === 'None')
                $(`#number_str${k}`).append(`<td id="date${k}">–</td>`)
            else
                $(`#number_str${k}`).append(`<td id="date${k}">${grades[i]['date']}</td>`)

            for (let j = 0; j < 10; j++) {
                if (grades[i][`parameter_${j}`]) {
                    if (grades[i][`parameter_${j}`] === '0')
                        $(`#number_str${k}`).append(`<td id="parameter_${j}${k}">–</td>`)
                    else
                        $(`#number_str${k}`).append(`<td id="parameter_${j}${k}">${grades[i][`parameter_${j}`]}</td>`)
                }
            }
            if (grades[i]['comment'] === 'None' || grades[i]['comment'] === '')
                $(`#number_str${k}`).append(`<td id="comment${k}">–</td>`)
            else
                $(`#number_str${k}`).append(`<td id="comment${k}">${grades[i]['comment']}</td>`)
        }
    }).fail(function () {
        alert('Error AJAX request')
    })
}

function sort(parameter, user_id) {

    if (sort.current_parameter === parameter) {
        sort.sort_up = !sort.sort_up
        $("#" + sort.current_parameter).attr("data-order") > 0 ?
            $("#" + sort.current_parameter).attr("data-order", "-1") :
            $("#" + sort.current_parameter).attr("data-order", "1")
    } else {
        sort.previous_parameter = sort.current_parameter
        sort.current_parameter = parameter
        sort.sort_up = true
        $("#" + sort.previous_parameter).attr("data-order", "0")
        $("#" + sort.current_parameter).attr("data-order") > 0 ?
            $("#" + sort.current_parameter).attr("data-order", "1") :
            $("#" + sort.current_parameter).attr("data-order", "-1")
    }

    $.post('/sort_grades_table_for_user', {
        parameter: parameter,
        sort_up: sort.sort_up,
        lim: limit,
        user_id: user_id
    }).done(
        function (response) {
            let grades = JSON.parse(response['grades'])
            let quantity = grades.length
            limit = quantity

            for (let i = 0; i < quantity; i++) {
                let k = i + 1
                $(`#date${k}`).html(grades[i]['date'] ? grades[i]['date'] : '–')

                for (let j = 0; j < 10; j++)
                    if ($(`#parameter_${j}${k}`))
                        $(`#parameter_${j}${k}`).html(grades[i][`parameter_${j}`] !== '0' ?
                            grades[i][`parameter_${j}`] : '–')

                $(`#comment${i++}`).html(grades[i][`comment`] ? grades[i][`comment`] : '–')

            }

        }).fail(function () {
        alert("Error AJAX request")
    })
}