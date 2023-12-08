use arbitrary::Unstructured;
use log::info;
use neo4rs::{query, ConfigBuilder};
use test_log::test;
use uuid::Uuid;

use crate::{
    db::neo4j::Neo4j,
    testutils::{round_trip, TestConfig},
};

fn get_db(_: Uuid) -> Neo4j {
    let config = TestConfig::load().unwrap();
    let user = config.neo4j_user;
    let pass = config.neo4j_password;
    let uri = config.neo4j_uri;
    info!("Connecting to {user}:{pass}@{uri}");
    Neo4j::new(
        ConfigBuilder::new()
            .user(&user)
            .password(&pass)
            .uri(&uri)
            .build()
            .expect("Invalid Neo4j configuration"),
    )
    .expect("Could not create Neo4j database")
}

#[test]
fn can_connect() {
    let neo4j = get_db(Uuid::new_v4());
    neo4j
        .run(query("SHOW USERS"))
        .expect("Failure to run query");
}

fn clear() {
    get_db(Uuid::new_v4())
        .run(query("MATCH (a) DETACH DELETE a"))
        .unwrap();
}

fn neo4j_round_trip(u: &mut Unstructured<'_>) -> arbitrary::Result<()> {
    clear();
    round_trip(u, get_db)
}

#[test]
fn test_round_trip() {
    let config = TestConfig::load().unwrap();
    arbtest::builder()
        .budget_ms(config.budget)
        .run(neo4j_round_trip);
}
