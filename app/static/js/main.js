function renderPageContent(evt){
    let targetPage;
    var ready = false;
    if(typeof evt === 'string'){
        targetPage = evt;
    }
    else {
        // Ignore are socket stuff for now

        // if(socket){
        //     socket.emit('stop_mosaic');
        // }
        targetPage = $(evt.target).attr('href');
    }


    targetPage = targetPage.slice(1);
    $.ajax({
        url: "/getPage?type=" + targetPage,
        dataType: 'html'
    }).done(function(response) {
        $('.page-content').html(response);
        MathJax.typeset();
    });
}

function submit_run(evt){
    console.log("called submit")
    // Get data from select fields format is [elementType]#[id]
    let eps = $('select#eps-select').val()
    let discount = $('select#discount-select').val()

    $.ajax({
        url: "/run_ajax",
        data: {'data': JSON.stringify({'eps': eps, 'discount': discount})},
        dataType: 'json'
    }).done(function(response) {
        // do something with results, this shows the response in console
        console.log(response)

        let newVidElm = $('<video id="first-vid" width="480" height="360" controls></video>')
            .append('<source type="video/mp4" />').attr({'src': response[0]});

        $('#first-vid').replaceWith(newVidElm);

    });

}

function render_result_list(response){
    console.log("Now rendering result list")

    let env_header_template = $('<div class="env-tab-header toggle-src" />');
    let env_content_template = $('<div class="env-tab-content toggle-target" style="display: none" />');
    let res_header_template = $('<div class="res-tab-header toggle-src" />');
    let res_content_template = $('<div class="res-tab-content toggle-target" style="display: none" />');

    let container = $('#result_list_container');

    for (const [key, value] of Object.entries(response)) {
        console.log(key);

        let env_tab_header = env_header_template.clone().text(key);
        let env_tab_content = env_content_template.clone();

        env_tab_header.attr({'data-target-ref': key});
        env_tab_content.attr({'data-src-ref': key});

        for (const [trick_key, tricks_res] of Object.entries(value)) {
            console.log(" --- " + trick_key)

            let trick_tab_header = res_header_template.clone().text(trick_key);
            let trick_tab_content = res_content_template.clone();

            trick_tab_header.attr({'data-target-ref': key + "_" + trick_key});
            trick_tab_content.attr({'data-src-ref': key + "_" + trick_key});

            for (const [seed_idx, seed_res] of Object.entries(tricks_res)) {

                let seed_tab_header = res_header_template.clone().text(seed_idx);
                let seed_tab_content = res_content_template.clone();

                seed_tab_header.attr({'data-target-ref': key + "_" + trick_key + "_" + seed_idx});
                seed_tab_content.attr({'data-src-ref': key +  "_" + trick_key + "_"  + seed_idx});

                if(seed_idx === 'grid_search'){
                    let heatmap_container_id = 'heatmap_' + key + "_" + trick_key;
                    let heatmap_container = $('<div />').attr({'id': heatmap_container_id})

                    init_heatmap(seed_res, heatmap_container, 'return', upper, lower);
                    seed_tab_content.append(heatmap_container);

                    // let heatmap_container_id2 = 'heatmap_growth_' + key + "_" + trick_key;
                    // let heatmap_container2 = $('<div />').attr({'id': heatmap_container_id2})
                    // init_heatmap(seed_res, heatmap_container2, 'growth');
                    // seed_tab_content.append(heatmap_container2);
                }
                else if(seed_idx === 'returns'){
                    let line_graph_id = 'linegraph_' + key + "_" + trick_key;
                    let line_graph_container = $('<div />').attr({'id': line_graph_id})
                    create_line_graph(seed_res, line_graph_container, line_graph_id);
                    seed_tab_content.append(line_graph_container);
                }
                else {
                    seed_tab_content.text(JSON.stringify(seed_res, null, 2))
                }

                trick_tab_content.append(seed_tab_header);
                trick_tab_content.append(seed_tab_content);
            }

            env_tab_content.append(trick_tab_header);
            env_tab_content.append(trick_tab_content);
        }

        container.append(env_tab_header);
        container.append(env_tab_content);
    }
}


function get_results_list(evt){
    console.log("called list results")

    $.ajax({
        url: "/list_results",
        contentType: "application/json",
        dataType: "json",
    }).done(function(response) {
        console.log("got the results from backend")
        render_result_list(response);
    }).fail((evt)=>{
        let test = JSON.parse(evt.responseText)
        console.log(test);
        console.log(evt)
        console.log("failed")
    });
}

function show_btn_target(evt){
    let src = $(evt.target);
    let target = src.attr('data-target-ref');

    $('.toggle-target[data-src-ref=' + target + ']').slideToggle()
}


// function render_data(data) {
//
//     var x = d3.scaleLinear()
//         .domain([1, 100])
//         .range([0, width]);
//     svg.append("g")
//         .attr("transform", "translate(0," + height + ")")
//         .call(d3.axisBottom(x));
//
//     var y = d3.scaleLinear()
//         .domain([0, 13])
//         .range([height, 0]);
//     svg.append("g")
//         .call(d3.axisLeft(y));
//
//     // Show confidence interval
//     svg.append("path")
//         .datum(data)
//         .attr("fill", "#cce5df")
//         .attr("stroke", "none")
//         .attr("d", d3.area()
//             .x(function (d) {
//                 return x(d.x)
//             })
//             .y0(function (d) {
//                 return y(d.CI_right)
//             })
//             .y1(function (d) {
//                 return y(d.CI_left)
//             })
//         )
//
//     // Add the line
//     svg
//         .append("path")
//         .datum(data)
//         .attr("fill", "none")
//         .attr("stroke", "steelblue")
//         .attr("stroke-width", 1.5)
//         .attr("d", d3.line()
//             .x(function (d) {
//                 return x(d.x)
//             })
//             .y(function (d) {
//                 return y(d.y)
//             })
//         )
//
// }
//
//
// function create_line_graph(data) {
//
//     // set the dimensions and margins of the graph
//     var margin = {top: 10, right: 30, bottom: 30, left: 60},
//         width = 460 - margin.left - margin.right,
//         height = 400 - margin.top - margin.bottom;
//
//     // append the svg object to the body of the page
//     var svg = d3.select("#my_dataviz")
//         .append("svg")
//         .attr("width", width + margin.left + margin.right)
//         .attr("height", height + margin.top + margin.bottom)
//         .append("g")
//         .attr("transform",
//             "translate(" + margin.left + "," + margin.top + ")");
//
//
// }


// let res_map = {
//    "id": "MountainCar_test1",
//     "conf": { "eps" : 0.3
//
//     }
// };


$('header').on('click', '.menu-item-id', renderPageContent);
// This means call submit_run once the element with id run_btn is clicked within the body element
let body = $('body');
body.on('click', '#run-btn', submit_run);
body.on('click', '#list_results_btn', get_results_list);
body.on('click', '.toggle-src', show_btn_target)
