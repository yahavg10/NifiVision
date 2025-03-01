from configurations.developer.developer_variables import container


def main():
    ds = container.get_service("DataSource")
    parser = container.get_service("Parser")
    trainer = container.get_service("Trainer")
    analyzer = container.get_service("Analyzer")

    raw_metrics = ds.get_metrics()
    parsed_metrics = parser.parse(raw_metrics)
    trained_model = trainer.train(parsed_metrics)
    analyzer.analyze(trained_model, X=parsed_metrics)
    x = 1


if __name__ == "__main__":
    main()