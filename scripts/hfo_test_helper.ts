// Medallion: Bronze | Mutation: 0% | HIVE: V
import config from './hfo_config.json';

export const getActiveUrl = (version?: string) => {
    const v = version || config.activeVersion;
    return `${config.baseUrl}${v}${config.suffix}`;
};
