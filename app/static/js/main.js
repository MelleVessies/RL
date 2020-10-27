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
        let heatmap_bounds = value.heatmap_bounds;
        let upper = heatmap_bounds.upper;
        let lower = heatmap_bounds.lower;

        for (const [trick_key, tricks_res] of Object.entries(value)) {
            console.log(" --- " + trick_key)

            let trick_tab_header = res_header_template.clone().text(trick_key);
            let trick_tab_content = res_content_template.clone();

            if (trick_key === "heatmap_bounds") {continue;}

            trick_tab_header.attr({'data-target-ref': key + "_" + trick_key});
            trick_tab_content.attr({'data-src-ref': key + "_" + trick_key});

            for (const [seed_idx, seed_res] of Object.entries(tricks_res)) {

                let seed_tab_header = res_header_template.clone().text(seed_idx);
                let seed_tab_content = res_content_template.clone();

                seed_tab_header.attr({'data-target-ref': key + "_" + trick_key + "_" + seed_idx});
                seed_tab_content.attr({'data-src-ref': key +  "_" + trick_key + "_"  + seed_idx});

                if(seed_idx === 'grid_search' || seed_idx === "mstd_grid"){
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


async function collect_graphs() {
    if(results === undefined) {
        await get_results_list();
    }
    $(".line-graph").each((idx, item)=>{
        let env = $(item).attr('data-env');
        let data;
        try {
            data = results[env]['all_tricks']['returns'];
        }
        catch{
            alert('failed to get results for ' + env + " from results list. Did you use the right indices?");
        }
        let line_graph_id = 'linegraph_' + env + "_" + "all_tricks_" + idx;
        let line_graph_container = $('<div />').attr({'id': line_graph_id});
        create_line_graph(data, line_graph_container, line_graph_id);
        item.replaceWith(line_graph_container.get(0));
    });
    $(".heatmap").each((idx, item)=>{
        let env = $(item).attr('data-env');
        let trick = $(item).attr('data-trick-id');
        let legend = !!$(item).attr('data-plot-legend');

        let upper;
        let lower;

        let data;
        try {
            data = results[env][trick]['grid_search'];

            let heatmap_bounds = results[env].heatmap_bounds;
            upper = heatmap_bounds.upper;
            lower = heatmap_bounds.lower;
        }
        catch{
            alert('failed to get results for ' + env + " and trick " + trick + " from results list. Did you use the right indices?");
        }
        let heatmap_container_id = 'heatmap_' + env + "_" + trick + "_" + idx;
        let heatmap_container = $('<div />').attr({'id': heatmap_container_id})

        init_heatmap(data, heatmap_container, 'return', upper, lower, legend, trick);
        item.replaceWith(heatmap_container.get(0));
    });


}

async function get_results_list(evt){
    console.log("called list results")

    await $.ajax({
        url: "/list_results",
        contentType: "application/json",
        dataType: "json",
    }).done(function(response) {
        console.log(response);
        results = response;
        render_result_list(response);
    });
}

function show_btn_target(evt){
    let src = $(evt.target);
    let target = src.attr('data-target-ref');

    $('.toggle-target[data-src-ref=' + target + ']').slideToggle()
}


$('header').on('click', '.menu-item-id', renderPageContent);
// This means call submit_run once the element with id run_btn is clicked within the body element
let body = $('body');
var results;

body.on('click', '#run-btn', submit_run);
body.on('click', '#list_results_btn', get_results_list);
body.on('click', '.toggle-src', show_btn_target)
